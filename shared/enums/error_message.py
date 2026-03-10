from enum import Enum

class ErrorMessageEnum(Enum):  
    UNAUTHORIZED = "unauthorized"
    INVALID_VERIFICATION_CODE = "invalid_verification_code"
    BAD_REQUEST = "bad_request"