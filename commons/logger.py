# coding: utf-8
import os
from datetime import datetime
from loguru import logger

log_path = './logs/'
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_file = '{0}/facedetect-{1}.log'.format(log_path, datetime.now().strftime('%Y-%m-%d'))

logger.add(log_file, rotation="12:00", retention="1 days", enqueue=True)
