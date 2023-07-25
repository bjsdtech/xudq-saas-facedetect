# 导入 FastAPI
from fastapi import APIRouter, UploadFile
import os
import cv2

from typing import Union
from enum import Enum
import base64


from models.models import Transaction
from models.crud import get_trans_by_trans_id
from db.database import get_db

from commons.logger import logger
from commons.common import write_file

from commons.result_code import ERROR_CODE
from commons.response_result import respones_result
from commons.response_result import face_detech_return
from commons.common import transid_generator
from commons.common import image_type_check


# create router
saas_facedetect_router = APIRouter(
    prefix='/{version}',
    tags=['version']
)


class PicType(str, Enum):
    url = "URL"
    base64 = "BASE64"


SERVICE_TYPE = '11'
DATA_FILE_PATH = './data/'
SAVE_FILE_PATH = './data/result/'
SRCS_FILE_PATH = './resources/'
FACE_CASCADE = './resources/the_face_cascade.xml'


@saas_facedetect_router.post("/facedetect/check")
async def faces_detect(version: str, picType: str, transId: str, timestamp: str, nonce: str,
                       file: Union[UploadFile, None] = None) -> dict:

    logger.info("(transid:"+transId+")face detect start.")
    logger.info("para:{" +
                "version:" + version +
                ", picType:" + picType +
                ", transId:" + transId +
                ", timestamp:" + timestamp +
                ", nonce:" + nonce + "}")

    if "" == picType.strip():
        logger.error("picType para is empty.")
        logger.info("(transid:" + transId + ")face detect end.")
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_PICTYPE_EMPTY.value, 4, "picType para is empty.")

    if "" == transId.strip():
        logger.error("transId is empty.")
        logger.info("(transid:" + transId + ")face detect end.")
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_TRANSID_EMPTY.value, 4, "transId is empty.")

    if "" == timestamp.strip():
        logger.error("timestamp para is empty.")
        logger.info("(transid:" + transId + ")face detect end.")
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_TIMESTAMP_EMPTY.value, 4, "timestamp para is empty.")

    if "" == nonce.strip():
        logger.error("nonce para is empty.")
        logger.info("(transid:" + transId + ")face detect end.")
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_NONCE_EMPTY.value, 4, "nonce para is empty.")

    if file is None:
        logger.error("image file para is empty.")
        logger.info("(transid:" + transId + ")face detect end.")
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_FILE_NONE.value, 4, "image file para is empty.")

    face_locations = []

    img_file_name = ""

    # status -- 检测结果: 1 - 检测成功， 2 - 检测失败，3 - 图片下载失败，4 - 图片格式错误，5 - 其他错误，请联系客服
    if not file:
        status = 3
        face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_FILE_NONE.value, status, "para(file) error.")
    else:
        contents = await file.read()
        img_file_name = file.filename
        # 保存原始图片文件
        write_file(DATA_FILE_PATH+img_file_name, contents)

    img_real_file = DATA_FILE_PATH + img_file_name
    # 对获得对图片校验
    result_split = img_file_name.split('.')
    if len(result_split) < 2:
        logger.error("image name format error.")
        logger.info("(transid:" + transId + ")face detect end.")
        status = 4
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_IMAGE_FORMAT.value, status, "image name format error.")

    # 获得图片文件的类型
    image_filetype = result_split[-1]

    if False == image_type_check(image_filetype):
        logger.error("image type error.")
        logger.info("(transid:" + transId + ")face detect end.")
        status = 4
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_IMAGE_TYPE.value, status, "image type error.")

    # 人脸检测逻辑
    img = cv2.imread(img_real_file)

    if "v1" == version:  # 版本v1 人脸检测

        # 人脸特征说明文件，计算机根据这些特征，进行人脸检测
        # 符合其中一部分特征，算作人脸
        face_detector = cv2.CascadeClassifier(FACE_CASCADE)

        # scaleFactor 缩放，默认 1.1   minNeighbors 默认 3，检测出来的人脸，就是坐标：x,y,w,h ，
        # faces = face_detector.detectMultiScale(img)
        # 检测黑白，显示彩色，数据变少提高效率
        gray = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6, minSize=(25, 25))
        face_number = len(faces)

        # 人脸的个数大于0，取出人脸坐标
        if face_number > 0:

            # faces 是二维的，可以用for 循环进行遍历取出
            for x, y, w, h in faces:
                # 矩形
                cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h), color=[0, 0, 255], thickness=2)

                # 圆形
                # cv2.circle(img,center=(x+w//2,y+h//2),radius=w//2, color=[0,255,0] )

                location = {"y1": str(y), "x1": str(x), "y2": str(y+h), "x2": str(x+w)}

                face_locations.append(location)

            # 检测结果 文件持久化
            inner_trans_id = transid_generator(SERVICE_TYPE)

            target_file_name = inner_trans_id+'.'+image_filetype
            target_real_file = SAVE_FILE_PATH+target_file_name

            cv2.imwrite(target_real_file, img)

            if os.path.exists(img_real_file):
                os.remove(img_real_file)

            # 检测记录入数据库表
            try:
                session = get_db()
                inner_channel_id = 11

                trans_data = Transaction(
                    is_deleted=1,
                    trans_id=inner_trans_id,
                    user_id="U123456789",
                    account_id="A0000000001",
                    request_id=transId,
                    from_channel=inner_channel_id,
                    raw_file_name=img_file_name,
                    file_type=11,
                    raw_file_path=img_real_file,
                    rst_file_name=target_file_name,
                    rst_file_path=target_real_file,
                    service_type=1,
                    fee_type=0,
                    fail_reason='',
                    status=4,
                    reserve_int_1=1,
                    reserve_char_1=''
                )
                session.add(trans_data)
                session.commit()
                session.close()

            except ArithmeticError:
                status = 2
                return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_DB_EXCEPT, status, "database except.")

            status = 1
            result = face_detech_return(transId, ERROR_CODE.FD_CHK_SUCCESS.value, status, "success", inner_trans_id, face_number, face_locations)

            logger.info("face_detect success: ")
            logger.info(result)
            logger.info("(transid:" + transId + ")face detect end.")
            return result
        else:
            status = 1
            result = face_detech_return(transId, ERROR_CODE.FD_CHK_SUCCESS.value, status, "success")
            logger.info("face_detect success:" + result)
            logger.info("(transid:" + transId + ")face detect end.")
            return result

    else:  # 接口版本号错误
        logger.error("version para error")
        logger.info("(transid:" + transId + ")face detect end.")
        status = 2
        return face_detech_return(transId, ERROR_CODE.FD_CHK_ERROR_VAR_NO_SUPPORT.value, status, "version must be v1")



@saas_facedetect_router.post("/facedetect/getcheckresult")
async def get_detect_result(version: str, picType: str, transId: str, timestamp: str, nonce: str) -> dict:

    logger.info("(transid:" + transId + ")get face detect result start.")

    logger.info("para:{" +
                "version:" + version +
                ", picType:" + picType +
                ", transId:" + transId +
                ", timestamp:" + timestamp +
                ", nonce:" + nonce + "}")

    # 版本v1 人脸检测
    if "v1" == version:

        if "" == picType.strip():
            logger.error("picType para is empty.")
            logger.info("(transid:" + transId + ")get face detect result end.")
            return respones_result(ERROR_CODE.FD_GET_ERROR_PICTYPE_EMPTY.value, "picType para is empty.")

        if "" == transId.strip():
            logger.error("transId is empty.")
            logger.info("(transid:" + transId + ")get face detect result end.")
            return respones_result(ERROR_CODE.FD_GET_ERROR_TRANSID_EMPTY.value, "transId para is empty.")

        if "" == timestamp.strip():
            logger.error("timestamp para is empty.")
            logger.info("(transid:" + transId + ")get face detect result end.")
            return respones_result(ERROR_CODE.FD_GET_ERROR_TIMESTAMP_EMPTY.value, "timestamp para is empty.")

        if "" == nonce.strip():
            logger.error("nonce para is empty.")
            logger.info("(transid:" + transId + ")get face detect result end.")
            return respones_result(ERROR_CODE.FD_GET_ERROR_NONCE_EMPTY.value, "nonce para is empty.")

        # 通过 transid 查数据库获得图片文件名
        try:
            # 添加数据
            session = get_db()

            trans_item = get_trans_by_trans_id(session, transId)

            if trans_item is None:
                result = {
                    "imageFile": '',
                    "requestId": transId
                }
                # resresult = respones_result(10110, "image no exists.", result)
                logger.error("image no exists, transId:"+transId)
                logger.info("(transid:" + transId + ")get face detect result end.")
                return respones_result(ERROR_CODE.FD_GET_ERROR_IMAGE_NO_EXISTS.value, "image no exists.", result)
            else:
                img_local_path = trans_item.rst_file_path

        except ArithmeticError:
            result = {
                "imageFile": '',
                "requestId": transId
            }

            logger.error("find image path from db except, transId:" + transId)
            logger.info("(transid:" + transId + ")get face detect result end.")
            return respones_result(ERROR_CODE.FD_GET_ERROR_DB_EXCEPT.value, "image no exists.", result)

        # 校验数据返回的文件是否还存在
        if os.path.exists(img_local_path):

            # file_open = open(img_local_path, 'rb')
            # img_stream_base64 = base64.b64encode(file_open.read()).decode()

            with open(img_local_path, 'rb') as img_file:
                img_stream_base64 = img_file.read()
                img_stream_base64 = base64.b64encode(img_stream_base64).decode()

            result = {
                "imageFile": img_stream_base64,
                "requestId": transId
            }

            resresult = respones_result(ERROR_CODE.FD_GET_SUCCESS.value, "success", result)
            logger.info("face_detect success.")
            logger.info("(transid:" + transId + ")get face detect result end.")
            # return render_template('./static/html/index.html', img_stream=img_stream_base64
            return resresult
        else:
            result = {
                "imageFile": '',
                "requestId": transId
            }

            logger.error("image no exists:"+img_local_path)
            logger.info("(transid:" + transId + ")get face detect result end.")
            return respones_result(ERROR_CODE.FD_GET_ERROR_FILE_DELETED.value, "image no exists", result)
    else:
        logger.error("version para error")
        logger.info("(transid:" + transId + ")face detect end.")
        return respones_result(ERROR_CODE.FD_GET_ERROR_FILE_DELETED.value, "version para error", )
