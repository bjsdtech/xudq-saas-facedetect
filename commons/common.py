import datetime
import random

SUPPORT_IMAGE_TYPE = ['jpg', 'png', 'jpeg']

# 11-图片人脸检测，12-图片人脸识别，21-证照OCR，22-票证OCR，31-音频检测，41-视频人脸检测，51-摄像头人脸检测
SUPPORT_SERVICE_TYPE = ['11', '12', '21', '22', '31', '41', '51']


def write_file(filename, data):
    with open(filename, 'wb') as wfile:
        wfile.write(data)


def image_type_check(filetype: str):
    if 0 == SUPPORT_IMAGE_TYPE.count(filetype):
        return False
    else:
        return True


def transid_generator(subtype: str):

    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if 0 == SUPPORT_SERVICE_TYPE.count(subtype):
        subtype = '00'

    new_trans_id = "T"+subtype+current_time + str(random.randint(100000, 999999))

    return new_trans_id
