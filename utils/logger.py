import logging
import os
from datetime import datetime
from pathlib import Path
import allure

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

class Logger:
    '''日志封装类，支持控制台输出、文件保存、Allure整合、截图功能'''

    def __init__(self,name: str = "selenium"):
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.INFO)

            if not self.logger.handlers:
                log_dir = os.path.join(os.getcwd(), "logs")
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, f"{datetime.now():%Y-%m-%d}.log")

                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                console_handler = logging.StreamHandler()

                formatter = logging.Formatter('%{asctime}s - %{levelname}s - %{message}s')
                file_handler.setFormatter(formatter)
                console_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)

            self.log_file = log_file

    def info(self,message: str):
        self.logger.info(message)
        allure.attach(message, name="log",attachment_type=allure.attachment_type.TEXT)

    def error(self,message: str):
        self.logger.error(message)
        allure.attach(message, name="Error",attachment_type=allure.attachment_type.TEXT)

    def attach_log_file(self):
        """附加完整日志文件到Allure"""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                allure.attach(f.read(), nmae = "Full Log File",attachment_type=allure.attachment_type.TEXT)

    def attach_screenshot(self,driver,name="Failure Screenshot"):
        """失败时截图并附加到 Allure"""
        screenshot_path = os.path.join(os.getcwd(), "logs",f"Screenshot_{datetime.now():%H%M%s}".PNG)
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name=name,attachment_type=allure.attachment_type.PNG)
        self.logger.error(f"测试失败，已截图保存至: {screenshot_path}")

    # 全局Logger实例
    Logger = Logger()


# def get_logger(name:str = "selenium"):
#     logger = logging.getLogger(name)
#
#     #避免重复添加handler
#     if logger.handlers:
#         return logger
#
#     logger.setLevel(logging.INFO)
#
#     #日志文件路径（按日期命名）
#     log_filename = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"
#
#     #文件日志输出
#     file_handler = logging.FileHandler(log_filename,encoding="utf-8")
#     file_handler.setLevel(logging.INFO)
#
#     #控制台输出
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#
#     formatter = logging.Formatter(
#         fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )
#
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
#
#     return logger