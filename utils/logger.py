import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / 'reports'
LOG_DIR = REPORT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "selenium.log"

def get_logger(name="selenium"):
    """
    获取一个标准的 logger 对象。
    name 参数用于区分不同模块对 logger 的使用。
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # 文件 Handler (每天轮转)
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

        # 控制台 Handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '%(name)s - %(levelname)s: %(message)s'
        ))
        logger.addHandler(stream_handler)

    return logger