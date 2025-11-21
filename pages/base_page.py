"""
文件作用：
-----------
BasePage 封装所有页面通用的 Selenium 操作：
包括 find 元素、click、type、visit 等。
其他页面类继承它，实现自己的业务逻辑。
"""
import os

import allure
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger, BASE_DIR
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = get_logger(self.__class__.__name__)  # 每个页面有独立 logger


    #查找元素
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    #点击元素
    @allure.step("点击元素 {locator}")
    def click(self, locator):
        self.logger.info(f"点击元素: {locator}")
        # 改用等待元素可点击
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

    #输入内容
    @allure.step("向元素 {locator} 输入内容: {text}")
    def send_keys(self, locator, text):
        self.logger.info(f"输入内容: {text} ")
        el = self.wait.until(EC.presence_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    #获取标题
    def get_title(self):
        return self.driver.title

    #获取文本
    def get_text(self, locator):
        # 使用封装了等待的 find_element 方法
        el = self.find_element(locator)
        text = el.text
        self.logger.info(f"获取元素 {locator} 文本: {text}")
        return text

    #截图功能
    def screenshot(self,name = "screenshot"):
        """失败时自动截图，并附加到Allure报告中"""

        # 假设截图目录基于项目根目录的绝对路径
        SCREENSHOT_DIR = BASE_DIR / "reports" / "screenshots"

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"{name}-{timestamp}.png"

        # 使用 Path 对象安全地拼接路径
        file_path = SCREENSHOT_DIR / file_name

        #创建目录
        os.makedirs(file_path.parent, exist_ok=True)

        #driver自带截图功能
        self.driver.save_screenshot(file_path)
        #把截图附加到Allure报告中
        with open(file_path, "rb") as f:
            allure.attach(f.read(), name=name, attachment_type=allure.attachmentType.PNG)

        print(f"[失败截图已保存]: {file_path}")

 # 可根据需要扩展更多方法