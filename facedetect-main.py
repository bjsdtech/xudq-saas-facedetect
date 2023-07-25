# 导入 FastAPI
from fastapi import FastAPI

import uvicorn

from apis.faces_detect_api import saas_facedetect_router

# 生成 FastAPI 类实例
saas_facedetect_app = FastAPI()


@saas_facedetect_app.get('/')
async def home() -> dict:
    return {
        "code": "000000",
        "msg": "Welcome to bjsdtech face detect SaaS ",
        "result: ": ""
    }


@saas_facedetect_app.post('/')
async def home() -> dict:
    return {
        "code": "000000",
        "msg": "Welcome to bjsdtech face detect SaaS ",
        "result: ": ""
    }

saas_facedetect_app.include_router(saas_facedetect_router)

if __name__ == '__main__':
    uvicorn.run(saas_facedetect_app, host='127.0.0.1', port=8083, log_level="info")
