from enum import Enum

class ERROR_CODE(str, Enum):

    SAAS_CHECKAUTHEN = "100000"

    # 人脸检测及查询 错误码 101100~101999
    # 101100~101999

    # 人脸检测 101100~101199
    FD_CHK_SUCCESS = "101100"
    FD_CHK_ERROR_VAR_EMPTY = "101111"
    FD_CHK_ERROR_VAR_NO_SUPPORT = "101112"
    FD_CHK_ERROR_PICTYPE_EMPTY = "101113"
    FD_CHK_ERROR_TRANSID_EMPTY = "101114"
    FD_CHK_ERROR_TIMESTAMP_EMPTY = "101115"
    FD_CHK_ERROR_NONCE_EMPTY = "101116"
    FD_CHK_ERROR_FILE_NONE = "101117"
    FD_CHK_ERROR_IMAGE_FORMAT = "101118"
    FD_CHK_ERROR_IMAGE_TYPE = "101119"
    FD_CHK_ERROR_DB_EXCEPT = "101120"

    # 人脸检测查询 101200~101299
    FD_GET_SUCCESS = "101200"
    FD_GET_ERROR_VAR_EMPTY = "101211"
    FD_GET_ERROR_VAR_NO_SUPPORT = "101211"
    FD_GET_ERROR_PICTYPE_EMPTY = "101212"
    FD_GET_ERROR_TRANSID_EMPTY = "101213"
    FD_GET_ERROR_TIMESTAMP_EMPTY = "101214"
    FD_GET_ERROR_NONCE_EMPTY = "101215"
    FD_GET_ERROR_IMAGE_NO_EXISTS = "101216"
    FD_GET_ERROR_DB_EXCEPT = "101217"
    FD_GET_ERROR_FILE_DELETED = "101218"

