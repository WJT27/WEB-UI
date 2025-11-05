import logging
import os
from datetime import datetime
from pathlib import Path
import allure

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name="selenium"):
    """
    获取一个标准的 logger 对象。
    name 参数用于区分不同模块对 logger 的使用。
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # 定义日志文件路径
        log_file = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def attach_screenshot(driver, name="Failure Screenshot"):
    """
    失败时截图并附加到 Allure 报告
    """
    screenshot_path = LOG_DIR / f"screenshot_{datetime.now():%H%M%S}.png"
    driver.save_screenshot(str(screenshot_path))
    allure.attach.file(str(screenshot_path), name=name, attachment_type=allure.attachment_type.PNG)


def attach_full_log():
    """
    把完整日志附加到 Allure 报告
    """
    log_file = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            allure.attach(f.read(), name="Full Log", attachment_type=allure.attachment_type.TEXT)