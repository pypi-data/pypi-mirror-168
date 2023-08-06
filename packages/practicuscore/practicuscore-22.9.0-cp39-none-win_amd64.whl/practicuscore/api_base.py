import os.path
import sys
from abc import ABC, abstractmethod
import platform
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import List, Optional, Union, cast

from dataclasses_json import dataclass_json, config

from practicuscore.cloud_def import CloudAuth, AWSCloudAuth
from practicuscore.core_def import PRTEng, PRTConn, CoreDef, OPResult


def exclude_if_none(value):
    return value is None


@dataclass_json
@dataclass
class PRTDataClass(ABC):
    def validate(self, log_error=True):
        # Validate all fields, if they have "validators" metadata.
        # if log_error == False, returns a tuple (field_name, error_message)
        #    intended to be used in UI to gracefully check issues without breaking
        # "validators" can be a single tuple (lambda_func, "err message") OR a list of validation tuples
        #    i.e. use a single validator:
        #     some_field: int = field(
        #         metadata={
        #             "validators": (lambda x: x > 0, "Must be > 0")
        #         })
        #    OR multiple validators:
        #     some_field: int = field(
        #         metadata={
        #             "validators": [(lambda x: x > 0, "Must be > 0"),
        #                            (lambda x: x < 10, "Must be < 10")]
        #         })
        # This method will also call validate() for children. (If a field has the validate() method)
        #    Meaning, field is a PRTDataClass itself potentially containing simple fields with "validators"
        for fld in fields(self):
            field_val = getattr(self, fld.name)

            sub_validate_func = getattr(field_val, "validate", None)
            if callable(sub_validate_func):
                # field is a PRTDataClass and has validate() method.
                field_val.validate()

            if "validators" in fld.metadata:
                validator_or_validators = fld.metadata["validators"]

                if isinstance(validator_or_validators, tuple):
                    validators = [validator_or_validators]
                else:
                    validators = validator_or_validators
                for validator_tuple in validators:
                    assert isinstance(validator_tuple, tuple), \
                        "Validator must be a tuple in the form of (validator_lambda, 'error message')"
                    validator_func, validator_err_msg = validator_tuple
                    field_val = getattr(self, fld.name)
                    try:
                        failed = False
                        if not validator_func(field_val):
                            failed = True
                    except Exception as ex:
                        failed = True
                        validator_err_msg = f"Exception occurred while checking for '{validator_err_msg}', " \
                                            f"\nException: {ex}"

                    if failed:
                        if log_error:
                            from practicuscore.core_conf import log_manager_glbl
                            logger = log_manager_glbl.get_logger()
                            logger.error(f"Validation for {self.__class__.__name__}.{fld.name}={field_val} "
                                         f"failed. \nError: {validator_err_msg}")
                            # the below can cause a crash
                            # raise ValueError(f"Validation for {self.__class__.__name__}.{fld.name}={field_val} "
                            #                  f"failed. \nError: {validator_err_msg}")
                        else:
                            return fld.name, validator_err_msg  # return info about first encountered issue
        if log_error:
            pass  # no issue, nothing to raise
        else:
            return None, None  # no issue, nothing to return

    def __post_init__(self):
        self.validate()


@dataclass_json
@dataclass
class FlexValidateDataClass(PRTDataClass, ABC):
    # In some rare cases we create empty dataclasses which has fields to be filled later.
    # for these, we cannot validate right after init.
    # If we add this flexibility to the base class, all json files end up having an unnecessary field
    bypass_validation: Optional[bool] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )

    def __post_init__(self):
        # Child classes validations metadata should work with default values, i.e. None
        # This will only work if values are passed part of init.
        # It is also possible fields are assigned value after init. In this case validate() should be called explicitly
        if not self.bypass_validation:
            self.validate()


@dataclass_json
@dataclass
class RequestMeta:
    meta_type: str = "Request"
    meta_name: str = ""
    req_time: Optional[datetime] = None
    req_core_v: str = CoreDef.CORE_VERSION
    req_os: str = platform.system()
    req_os_v: str = platform.release()
    req_py_minor_v: int = sys.version_info.minor


@dataclass_json
@dataclass
class PRTRequest(PRTDataClass, ABC):
    # Creating meta class here caused a nasty bug. meta became a shared object between child classes
    #   i.e. when __post_init() below updated meta_name for one type of Request class, al others got the new name
    # meta: RequestMeta = RequestMeta()
    meta: Optional[RequestMeta] = None

    @property
    def name(self) -> str:
        return self.meta.meta_name

    def __post_init__(self):
        self.meta = RequestMeta()
        self.meta.meta_name = self.__class__.__name__.rsplit("Request", 1)[0]
        # do not assign defaults in class definition. Gets assigned static one time
        self.meta.req_time = datetime.utcnow()
        super().__post_init__()


@dataclass_json
@dataclass
class ResponseMeta:
    meta_type: str = "Response"
    meta_name: str = ""
    resp_node_v: str = ""  # assigned later right before sending to client
    resp_py_minor_v: int = sys.version_info.minor


@dataclass_json
@dataclass
class PRTResponse(PRTDataClass, ABC):
    meta: Optional[ResponseMeta] = None
    op_result: Optional[OPResult] = None
    # meta: ResponseMeta = ResponseMeta()  Don't instantiate here. Read notes for PRTRequest

    @property
    def name(self) -> str:
        return self.meta.meta_name

    def __post_init__(self):
        self.meta = ResponseMeta()
        self.meta.meta_name = self.__class__.__name__.rsplit("Response", 1)[0]
        # do not assign defaults in class definition. Gets assigned static one time
        self.meta.req_time = datetime.utcnow()
        super().__post_init__()


@dataclass_json
@dataclass
class EmptyResponse(PRTResponse):
    # used when there's an error, no response can be created and we hae op_result send back
    pass


# Connection configuration classes

@dataclass
class UIMap:
    # Helps map an individual ConnConf field to a single GUI element.
    # i.e. MYSQL related field "db_host" should be visible as "Database Host Address", it is required, ...
    visible_name: Optional[str] = None
    auto_display: bool = True  # some fields are displayed manually and not automated
    tip: Optional[str] = None
    default_value: Optional[str] = None
    is_required: bool = True
    is_password: bool = False


@dataclass_json
@dataclass
class ConnConf(FlexValidateDataClass, ABC):
    sampling_method: Optional[str] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )
    sample_size: Optional[int] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )
    sample_size_app: Optional[int] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )
    column_list: Optional[List[str]] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )
    filter: Optional[str] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )
    ws_uuid: Optional[str] = field(
        default=None,
        metadata=config(exclude=exclude_if_none),
    )

    @property
    def conn_type(self) -> PRTConn:
        return self._conn_type

    @property
    def friendly_desc(self) -> str:
        # override with children class for a better user friendly
        return f"Cloud {self._conn_type}"

    @property
    def friendly_long_desc(self) -> str:
        return self.friendly_desc

    @property
    def audit_desc(self) -> str:
        # override with children class for audit
        return self.friendly_desc

    def copy_secure(self) -> 'ConnConf':
        import copy
        return copy.copy(self)

    def copy_with_credentials(self, auth: CloudAuth, additional_credentials: Optional[dict] = None) -> 'ConnConf':
        return self.copy_secure()

    @abstractmethod
    def _equals(self, other: 'ConnConf') -> bool:
        pass

    def __eq__(self, other: 'ConnConf') -> bool:
        if not isinstance(other, ConnConf):
            return False
        other = cast(ConnConf, other)
        equals = self.conn_type == other.conn_type \
                 and self.sample_size == other.sample_size \
                 and self.sample_size_app == other.sample_size_app \
                 and self.column_list == other.column_list \
                 and self.filter == other.filter
        if not equals:
            return False
        return self._equals(other)


@dataclass_json
@dataclass
class InMemoryConnConf(ConnConf):
    _conn_type: PRTConn = PRTConn.IN_MEMORY
    df: Optional[object] = None

    @property
    def friendly_desc(self) -> str:
        return "In memory dataframe"

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, InMemoryConnConf):
            return False
        other = cast(InMemoryConnConf, other)
        return self.df.__eq__(other.df)


@dataclass_json
@dataclass
class LocalFileConnConf(ConnConf):
    _conn_type: PRTConn = PRTConn.LOCAL_FILE
    file_path: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="File Path",
                        tip="Type path on local disk")
    })

    @property
    def friendly_desc(self) -> str:
        try:
            if self.file_path:
                return os.path.splitext(os.path.basename(self.file_path))[0]
        except:
            pass

        return self._conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        return f"Local file: {self.file_path}"

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, LocalFileConnConf):
            return False
        other = cast(LocalFileConnConf, other)
        return self.file_path == other.file_path


@dataclass_json
@dataclass
class NodeFileConnConf(ConnConf):
    _conn_type: PRTConn = PRTConn.NODE_FILE
    file_path: Optional[str] = field(default=None, metadata={
        "ui_map": UIMap(visible_name="File Path",
                        tip="Type path on node local disk. E.g. /home/ubuntu/data/file.csv")
    })

    @property
    def friendly_desc(self) -> str:
        try:
            if self.file_path:
                return os.path.splitext(os.path.basename(self.file_path))[0]
        except:
            pass

        return self._conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        return f"Cloud node file: {self.file_path}"

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, NodeFileConnConf):
            return False
        other = cast(NodeFileConnConf, other)
        return self.file_path == other.file_path


@dataclass_json
@dataclass
class S3ConnConf(ConnConf):
    _conn_type: PRTConn = PRTConn.S3
    aws_region: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    s3_bucket: Optional[str] = None
    s3_keys: Optional[List[str]] = None

    @property
    def friendly_desc(self) -> str:
        try:
            if self.s3_keys:
                if len(self.s3_keys) >= 1:
                    s3_key = self.s3_keys[0]
                    if s3_key.find(".") > -1:
                        return os.path.splitext(os.path.basename(s3_key))[0]
                    else:
                        return os.path.basename(os.path.normpath(s3_key))
        except:
            pass
        return self._conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        bucket_desc = f"s3://{self.s3_bucket}"
        if self.s3_keys:
            if len(self.s3_keys) == 1:
                return f"{bucket_desc}/{self.s3_keys[0]}"
            else:
                return f"{bucket_desc}/{self.s3_keys[0]} .."
        return bucket_desc

    @property
    def audit_desc(self) -> str:
        if self.s3_bucket:
            s3_info = self.s3_bucket
            if self.s3_keys:
                for s3_key in self.s3_keys:
                    s3_info += " " + s3_key
            return s3_info
        return ""

    def copy_secure(self) -> ConnConf:
        copy_conn_conf = super().copy_secure()
        assert isinstance(copy_conn_conf, S3ConnConf)
        copy_conn_conf = cast(S3ConnConf, copy_conn_conf)
        copy_conn_conf.aws_access_key_id = None
        copy_conn_conf.aws_secret_access_key = None
        copy_conn_conf.aws_session_token = None
        return copy_conn_conf

    def copy_with_credentials(self, auth: CloudAuth, additional_credentials: Optional[dict] = None) -> ConnConf:
        copy_conn_conf = super().copy_secure()
        copy_conn_conf = cast(S3ConnConf, copy_conn_conf)
        if not isinstance(auth, AWSCloudAuth):
            return copy_conn_conf
        auth = cast(AWSCloudAuth, auth)
        copy_conn_conf.aws_access_key_id = auth.aws_access_key_id
        copy_conn_conf.aws_secret_access_key = auth.aws_secret_access_key
        copy_conn_conf.aws_session_token = auth.aws_session_token
        return copy_conn_conf

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, S3ConnConf):
            return False
        other = cast(S3ConnConf, other)
        return self.aws_region == other.aws_region \
               and self.aws_access_key_id == other.aws_access_key_id \
               and self.aws_secret_access_key == other.aws_secret_access_key \
               and self.aws_session_token == other.aws_session_token \
               and self.s3_bucket == other.s3_bucket \
               and self.s3_keys == other.s3_keys


@dataclass_json
@dataclass
class RelationalConnConf(ConnConf, ABC):
    sql_query: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="SQL Query",
                        auto_display=False),
        "validators": (lambda x: x and len(x) > 0, "No SQL query provided")
    })

    target_table_name: Optional[str] = None

    def _find_table_name(self, keyword: str) -> Optional[str]:
        if self.sql_query:
            table_ind = self.sql_query.lower().find(f"{keyword} ") + len(f"{keyword} ")
            if table_ind > -1:
                desc = self.sql_query[table_ind:].strip().lower()
                desc = desc[:desc.find(" ")].strip()
                if desc:
                    return desc
        return None

    @property
    def friendly_desc(self) -> str:
        try:
            table_name = self._find_table_name("from")
            if not table_name:
                table_name = self._find_table_name("into")

            if table_name:
                return table_name

            if self.sql_query:
                return self.sql_query[:10] + f"{'..' if len(self.sql_query) > 10 else ''}"
        except:
            pass
        return self._conn_type.lower()

    @property
    def friendly_long_desc(self) -> str:
        table_name = self._find_table_name("from")
        if table_name:
            desc = f"table: {table_name}"
        else:
            desc = ":"
        desc += f" ({self.sql_query[:30]}{'...' if len(self.sql_query) > 30 else ''})"
        desc = desc.replace("\n", " ")
        return f"{self._conn_type.lower()} {desc}"

    @property
    def audit_desc(self) -> str:
        audit_info = self.friendly_desc
        if self.sql_query:
            audit_info += "\nSQL: " + self.sql_query

        return audit_info

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, RelationalConnConf):
            return False
        other = cast(RelationalConnConf, other)
        return self.sql_query == other.sql_query and self.target_table_name == other.target_table_name


@dataclass_json
@dataclass
class SqLiteConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.SQLITE
    file_path: str = field(default="None", metadata={
        "ui_map": UIMap(visible_name="File Path",
                        tip="Type path on node local disk. E.g. /home/ubuntu/data/database.db",
                        default_value="/home/ubuntu/samples/chinook.db"),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, SqLiteConnConf):
            return False
        other = cast(SqLiteConnConf, other)
        return self.file_path == other.file_path


@dataclass_json
@dataclass
class MYSQLConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.MYSQL
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="3306"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, MYSQLConnConf):
            return False
        other = cast(MYSQLConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"MySQL Host:{self.db_host} DB:{self.db_name} User:{self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class PostgreSQLConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.POSTGRESQL
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="5432"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, PostgreSQLConnConf):
            return False
        other = cast(PostgreSQLConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"PostgreSQL Host:{self.db_host} DB:{self.db_name} User:{self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class RedshiftConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.REDSHIFT
    # redshift_db_address: Optional[str] = None  # dummy
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="5439"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, RedshiftConnConf):
            return False
        other = cast(RedshiftConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"Redshift Host:{self.db_host} DB:{self.db_name} User:{self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class SnowflakeConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.SNOWFLAKE
    # redshift_db_address: Optional[str] = None  # dummy

    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    schema: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Schema",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    warehouse_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Warehouse Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    role: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Role",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    account: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Account Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        ),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, SnowflakeConnConf):
            return False
        other = cast(SnowflakeConnConf, other)
        return self.db_name == other .db_name \
               and self.schema == other .schema \
               and self.warehouse_name == other .warehouse_name \
               and self.user == other .user \
               and self.role == other.role \
               and self.account == other.account \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"Snowflake Warehouse:{self.warehouse_name} DB:{self.db_name} Schema:{self.schema} " \
                      f"User:{self.user} Role:{self.role} Account:{self.account}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class MSSQLConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.MSSQL
    # redshift_db_address: Optional[str] = None  # dummy
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    # driver: str = field(default=None, metadata={
    #     "ui_map": UIMap(visible_name="Driver Name",
    #                     default_value="SQL Server Native Client 10.0"),
    #     "validators": (lambda x: x and len(x) > 0, "No value provided")
    # })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="1433"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, MSSQLConnConf):
            return False
        other = cast(MSSQLConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"MSSQL Host:{self.db_host} DB:{self.db_name} User:{self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class OracleConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.ORACLE
    # redshift_db_address: Optional[str] = None  # dummy
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    # driver: str = field(default=None, metadata={
    #     "ui_map": UIMap(visible_name="Driver Name",
    #                     default_value="SQL Server Native Client 10.0"),
    #     "validators": (lambda x: x and len(x) > 0, "No value provided")
    # })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="1521"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, OracleConnConf):
            return False
        other = cast(OracleConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"Oracle Host:{self.db_host} DB:{self.db_name} User:{self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class HiveHadoopConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.HIVE_HADOOP
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value=""),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, HiveHadoopConnConf):
            return False
        other = cast(HiveHadoopConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"Hive Host:{self.db_host} DB:{self.db_name}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class AthenaConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.ATHENA
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test.abcde.us-east-1.rds.amazonaws.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_name: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    s3_dir: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="S3 Location",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="443"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    access_key: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Access key ID",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    secret_key: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="AWS Secret access key",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, AthenaConnConf):
            return False
        other = cast(AthenaConnConf, other)
        return self.db_host == other.db_host \
               and self.db_name == other .db_name \
               and self.s3_dir == other .s3_dir \
               and self.db_port == other.db_port \
               and self.access_key == other.access_key \
               and self.secret_key == other.secret_key

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"Athena Host:{self.db_host} DB:{self.db_name}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class ElasticSearchConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.ELASTIC_SEARCH
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. test-2.latest-elasticsearch.abc-3.xyz.com or 192.168.0.1",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value=""),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, ElasticSearchConnConf):
            return False
        other = cast(ElasticSearchConnConf, other)
        return self.db_host == other.db_host \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"Elastic :{self.db_host} DB:{self.db_port} User: {self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class AWSElasticSearchConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.AWS_ELASTIC_SEARCH
    db_host: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Database Server Address",
                        tip="E.g. search-test-abcde.us-east-1.es.amazonaws.com",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    db_port: int = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Port",
                        default_value="443"),
        "validators": (lambda x: 1 <= int(x) <= 65_535, "Port must be between 1 and 65,535")
    })
    user: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="User Name",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })
    password: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Password",
                        is_password=True,
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, AWSElasticSearchConnConf):
            return False
        other = cast(AWSElasticSearchConnConf, other)
        return self.db_host == other.db_host \
               and self.db_port == other.db_port \
               and self.user == other.user \
               and self.password == other.password

    @property
    def audit_desc(self) -> str:
        audit_info = ""
        audit_info += f"AWS OpenSearch :{self.db_host} DB:{self.db_port} User: {self.user}"
        if self.sql_query:
            audit_info += " SQL: " + self.sql_query

        return audit_info


@dataclass_json
@dataclass
class CustomDBConnConf(RelationalConnConf):
    _conn_type: PRTConn = PRTConn.CUSTOM_DB
    # redshift_db_address: Optional[str] = None  # dummy
    conn_string: str = field(default=None, metadata={
        "ui_map": UIMap(visible_name="Connection String",
                        tip="Any SQLAlchemy compatible db conn str (might require driver installation)",
                        default_value=""),
        "validators": (lambda x: x and len(x) > 0, "No value provided")
    })

    def _equals(self, other: 'ConnConf') -> bool:
        if not isinstance(other, CustomDBConnConf):
            return False
        other = cast(CustomDBConnConf, other)
        return self.conn_string == other.conn_string

    @property
    def audit_desc(self) -> str:
        return f"Custom DB Connection with connection string (can include password)"


class ConnConfFactory:
    @staticmethod
    def create_or_get(conn_conf_json_dict_or_obj) -> ConnConf:
        # due to json serialization this method can get json, dict or actual class
        if isinstance(conn_conf_json_dict_or_obj, str):
            import json
            conn_conf_json_dict_or_obj = json.loads(conn_conf_json_dict_or_obj)

        if isinstance(conn_conf_json_dict_or_obj, dict):
            conn_type_str = conn_conf_json_dict_or_obj['_conn_type']
            if conn_type_str == PRTConn.LOCAL_FILE:
                return LocalFileConnConf.from_dict(conn_conf_json_dict_or_obj)
            if conn_type_str == PRTConn.NODE_FILE:
                return NodeFileConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.S3:
                return S3ConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.SQLITE:
                return SqLiteConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.MYSQL:
                return MYSQLConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.POSTGRESQL:
                return PostgreSQLConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.REDSHIFT:
                return RedshiftConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.SNOWFLAKE:
                return SnowflakeConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.MSSQL:
                return MSSQLConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.ORACLE:
                return OracleConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.HIVE_HADOOP:
                return HiveHadoopConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.ATHENA:
                return AthenaConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.ELASTIC_SEARCH:
                return ElasticSearchConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.AWS_ELASTIC_SEARCH:
                return AWSElasticSearchConnConf.from_dict(conn_conf_json_dict_or_obj)
            elif conn_type_str == PRTConn.CUSTOM_DB:
                return CustomDBConnConf.from_dict(conn_conf_json_dict_or_obj)
            else:
                raise AttributeError(f"Unknown connection type {conn_type_str}")
        elif issubclass(type(conn_conf_json_dict_or_obj), ConnConf):
            return conn_conf_json_dict_or_obj
        else:
            raise SystemError(f"Unknown conn_conf type {type(conn_conf_json_dict_or_obj)}")


# Engine Configuration Classes
@dataclass_json
@dataclass
class EngConf(PRTDataClass, ABC):
    @property
    def eng_type(self) -> PRTEng:
        return self._eng_type


@dataclass_json
@dataclass
class PandasEngConf(EngConf):
    _eng_type: PRTEng = PRTEng.PANDAS


@dataclass_json
@dataclass
class DaskEngConf(PandasEngConf):
    _eng_type: PRTEng = PRTEng.DASK
    worker_count: Optional[int] = None


@dataclass_json
@dataclass
class RapidsEngConf(PandasEngConf):
    _eng_type: PRTEng = PRTEng.RAPIDS


@dataclass_json
@dataclass
class RapidsDaskEngConf(DaskEngConf):
    _eng_type: PRTEng = PRTEng.RAPIDS_DASK
    worker_count: Optional[int] = None


@dataclass_json
@dataclass
class SparkEngConf(PandasEngConf):
    _eng_type: PRTEng = PRTEng.SPARK


class EngConfFactory:
    @staticmethod
    def create(eng_conf_json_dict_or_obj) -> EngConf:
        # due to json serialization this method can get json, dict or actual class
        if not eng_conf_json_dict_or_obj:
            return PandasEngConf()

        if isinstance(eng_conf_json_dict_or_obj, str):
            if eng_conf_json_dict_or_obj.strip().startswith("{"):
                import json
                eng_conf_json_dict_or_obj = json.loads(eng_conf_json_dict_or_obj)
            else:
                # simple engine name, might be coming from exported code library
                eng_conf_json_dict_or_obj = {'_eng_type': eng_conf_json_dict_or_obj}

        if isinstance(eng_conf_json_dict_or_obj, dict):
            eng_type_str = str(eng_conf_json_dict_or_obj['_eng_type']).upper()
            if eng_type_str == PRTEng.PANDAS:
                return PandasEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.DASK:
                return DaskEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.RAPIDS:
                return RapidsEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.RAPIDS_DASK:
                return RapidsDaskEngConf.from_dict(eng_conf_json_dict_or_obj)
            elif eng_type_str == PRTEng.SPARK:
                return SparkEngConf.from_dict(eng_conf_json_dict_or_obj)
            else:
                raise AttributeError(f"Unknown engine type {eng_type_str}")
        elif isinstance(eng_conf_json_dict_or_obj, EngConf):
            return eng_conf_json_dict_or_obj
        else:
            raise SystemError(f"Unknown eng_conf type {type(eng_conf_json_dict_or_obj)}")


@dataclass_json
@dataclass
class PRTDataRequest(PRTRequest):
    # ** We needed to add dict to this list since when dataclass_json cannot figure out type
    #    it returns dict instead of actual class. need to override or use as dict
    conn_conf: Union[
        dict,
        NodeFileConnConf,
        SqLiteConnConf,
        S3ConnConf,
        MYSQLConnConf,
        PostgreSQLConnConf,
        RedshiftConnConf,
        SnowflakeConnConf,
        MSSQLConnConf,
        OracleConnConf,
        HiveHadoopConnConf,
        AthenaConnConf,
        ElasticSearchConnConf,
        AWSElasticSearchConnConf,
        CustomDBConnConf,
    ] = field(default=None, metadata={
        "validators": (lambda x: isinstance(x, dict) or isinstance(x, ConnConf), "conn_conf dict or class not provided")
    })

    eng_conf: Optional[Union[
        dict,
        PandasEngConf,
        DaskEngConf,
        RapidsEngConf,
        RapidsDaskEngConf,
        SparkEngConf,
    ]] = field(default=None, metadata={
        "validators": (lambda x: x is None or isinstance(x, dict) or isinstance(x, EngConf),
                       "eng_conf must be None, a dict or subclass of EngConf")
    })

    # MySQLConnDef,
    # AuroraMySQLConnDef,


if __name__ == "__main__":
    pass
    # eng_conf = RapidsDaskEngConf()
    # eng_conf = EngConfFactory.create(eng_conf)
    # print(eng_conf)
