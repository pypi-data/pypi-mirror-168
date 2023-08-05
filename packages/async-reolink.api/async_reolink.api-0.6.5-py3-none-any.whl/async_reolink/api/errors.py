"""Common Errors"""

from __future__ import annotations

from enum import Enum
from typing import Final


class ErrorCode(int):
    """Expanded Error Code"""

    def __new__(cls, code: int, *_):
        return super().__new__(cls, code)

    def __init__(self, _, label: str, description: str):
        super().__init__()
        self.label = label
        self.description = description


# this is raw from the API sheet, needs language cleanup
class ErrorCodes(ErrorCode, Enum):
    """Error Codes"""

    MISSING_PARAMETERS = (-1, "not exist", "Missing parameters")
    OUT_OF_MEMORY = (-2, "out of mem", "Used up memory")
    CHECK_ERROR = (-3, "check err", "Check error")
    PARAMETER_ERROR = (-4, "param error", "Parameters error")
    SESSION_MAX = (-5, "max session", "Reached the max session number.")
    AUTH_REQUIRED = (-6, "please login first", "Login required")
    LOGIN_FAILED = (-7, "login failed", "Login error")
    TIMEOUT = (-8, "timeout", "Operation timeout")
    NOT_SUPPORTED = (-9, "not support", "Not supported")
    PROTOCOL_ERROR = (-10, "protocol", "Protocol error")
    READ_FAILED = (-11, "fcgi read failed", "Failed to read operation")
    GET_CONFIG = (-12, "get config failed", "Failed to get configuration.")
    SET_CONFIG = (-13, "set config failed", "Failed to set configuration.")
    MALLOC = (-14, "malloc failed", "Failed to apply for memory")
    CREATE_SOCKET = (-15, "create socket failed", "Failed to created socket")
    SEND_DATA = (-16, "send failed", "Failed to send data")
    RECV_DATA = (-17, "rcv failed", "Failed to receiver data")
    OPEN_FILE = (-18, "open file failed", "Failed to open file")
    READ_FILE = (-19, "read file failed", "Failed to read file")
    WRITE_FILE = (-20, "write file failed", "Failed to write file")
    TOKEN = (-21, "error token", "Token error")
    STR_LEN = (
        -22,
        "The length of the string exceeds the limit",
        "The length of the string exceeds the limitmation",
    )
    MISSING_PARAMETER = (-23, "missing param", "Missing parameters")
    COMMAND = (-24, "error command", "Command error")
    INTERNAL = (-25, "internal error", "Internal error")
    ABILITY = (-26, "ability error", "Ability error")
    INVALID_USER = (-27, "invalid user", "Invalid user")
    USER_EXISTS = (-28, "user already exist", "User already exist")
    MAX_USERS = (
        -29,
        "maximum number of users",
        "Reached the maximum number of users",
    )
    SAME_VERSION = (-30, "same version",
                    "The version is identical to the current one.")
    BUSY = (-31, "busy", "Ensure only one user can upgrade")
    IP_CONFLICT = (-32, "ip conflict", "Modify IP conflicted with used IP")
    CLOUD_EMAIL = (-34, "need bing email", "Cloud login need bind email first")
    CLOUD_LOGIN_UNBIND = (-35, "unbind", "Cloud login unbind camera")
    CLOUD_TIMEOUT = (
        -36,
        "network timeout",
        "Cloud login get login information out of time",
    )
    CLOUD_PASSWORD = (-37, "password err", "Cloud login password error")
    CLOUD_UID = (-38, "uid err", "Cloud bind camera uid error")
    CLOUD_USER = (-39, "user not exist", "Cloud login user doesn’t exist")
    CLOUD_UNBIND = (-40, "unbind failed", "Cloud unbind camera failed")
    CLOUD_NOT_USSPORTED = (-41, "cloud not support",
                           "The device doesn’t support cloud")
    CLOUD_LOGIN = (-42, "login cloud server failed",
                   "Cloud login server failed")
    CLOUD_BIND = (-43, "bind failed", "Cloud bind camera failed")
    CLOUD_UNKNOWN = (-44, "cloud unknown err", "Cloud unknown error")
    CLOUD_VERIFY = (-45, "need verify code",
                    "Cloud bind camera need verify code")
    SNAP_FAILED = (-48, "Fetching a picture failed", "Snap a picture failed")
    INVALID_CHANNEL = (-49, "Channel invalid", "Channel is invalid")
    EMPTY = (-99, "", "")
    TEST = (-100, "test failed", "Test Email、Ftp、Wifi failed")
    UPGRADE_CHECK = (-101, "check firmware failed",
                     "Upgrade checking firmware failed")
    UPGRADE_DOWNLOAD = (
        -102,
        "download online failed",
        "Upgrade download online failed",
    )
    UPGRADE_STATUS = (
        -103,
        "get upgrade status failed",
        "Upgrade get upgrade status failed",
    )
    TO_MANY_LOGINS = (
        -105,
        "Frequent logins, please try again later!",
        "Frequent logins",
    )
    FTP_TEST = (-451, "ftp login failed", "ftp test login failed")
    FT_CREATE = (-452, "ftp create dir failed", "Creat ftp dir failed")
    FTP_UPLOAD = (-453, "ftp upload failed", "Upload ftp file failed")
    FTP = (-454, "ftp connect failed", "Cannot connect ftp server")
    EMAIL_UNKNOWN = (-480, "email undefined failed", "Some undifined errors")
    EMAIL_CONNECT = (-481, "email connect failed",
                     "Cannot connect email server")
    EMAIL_AUTH = (-482, "email auth failed", "Auth user failed")
    EMAIL = (-483, "email network err", "Email network err")
    EMAIL_SERVER = (-484, "email server err",
                    "Something wrong with email server")
    EMAIL_MEMORY = (-485, "email memory err", "Something wrong with memory")
    PASSWORD_WRONG = (-502, "password is wrong",
                      "The password you provided is incorrect.")


class ReolinkError(Exception):
    """Base Error Class"""


class ReolinkConnectionError(ReolinkError):
    """ReoLink Connection Error"""


class ReolinkTimeoutError(ReolinkError):
    """Reolink Operation Timeout"""


class ReolinkResponseError(ReolinkError):
    """Reolink Response Error"""

    def __init__(
        self, *args: object, code: ErrorCodes | int | None = None, details: str | None = None
    ) -> None:
        super().__init__(*args, details or (code.description if code is not None else None))
        self._code = code
        self._details = details

    @property
    def code(self):
        """Error Code"""
        return self._code

    @property
    def details(self):
        """Error Details"""
        return self._details


class ReolinkStreamResponseError(ReolinkResponseError):
    """Reolink Stream Response  Error"""

    DEFAULT_DETAILS: Final = "Expected a stream response"

    def __init__(
        self,
        *args: object,
        code: ErrorCodes = ErrorCodes.READ_FAILED,
        details: str = DEFAULT_DETAILS,
    ) -> None:
        super().__init__(*args, code=code, details=details)


class ReolinkUnhandledError(ReolinkError):
    """Reolink Unhandled Expcetion"""
