import logging
import os
from datetime import datetime
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = BASE_DIR / 'reports'
LOG_DIR = REPORT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name="selenium"):
    """
    获取一个标准的 logger 对象。
    name 参数用于区分不同模块对 logger 的使用。
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        log_file = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# 创建全局 logger 实例
logger = get_logger("selenium")