"""
文件作用：
-----------
BasePage 封装所有页面通用的 Selenium 操作：
包括 find 元素、click、type、visit 等。
其他页面类继承它，实现自己的业务逻辑。
"""
import os

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import load_config
from utils.logger import get_logger, BASE_DIR


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.config = load_config()
        # 显式等待时间使用配置中的隐式等待时间
        self.wait = WebDriverWait(driver, self.config.get("implicitly_wait", 10))
        self.logger = get_logger(self.__class__.__name__)

    @allure.step("访问 URL: {url}")
    def visit(self, url=""):
        """访问完整的 URL"""
        full_url = self.config['base_url'] + url
        self.logger.info(f"访问页面: {full_url}")
        self.driver.get(full_url)

    def _wait_for_visibility(self, locator):
        """等待元素可见"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    #查找元素
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("点击元素: {locator}")
    def click(self, locator):
        """等待元素可点击并执行点击操作"""
        self.logger.info(f"点击元素: {locator}")
        # 优化：等待元素可点击
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()

    @allure.step("输入内容 '{text}' 到元素: {locator}")
    def send_keys(self, locator, text):
        """等待元素可见，清空并输入文本"""
        self.logger.info(f"输入内容 '{text}' 到元素: {locator}")
        el = self._wait_for_visibility(locator)
        el.clear()
        el.send_keys(text)
        el.send_keys(text)

    def get_title(self):
        """获取页面标题"""
        title = self.driver.title
        self.logger.info(f"获取页面标题: {title}")
        return title

    def get_text(self, locator):
        """获取元素的文本"""
        # 优化：使用封装的等待方法
        text = self._wait_for_visibility(locator).text
        self.logger.info(f"获取元素 {locator} 文本: {text}")
        return text

# --- 增强断言方法 ---
    @allure.step("断言：检查页面标题是否包含文本 '{expected_text}'")
    def assert_title_contains(self, expected_text):
        """断言当前页面标题是否包含指定文本"""
        current_title = self.get_title()
        assert expected_text in current_title, f"标题断言失败！期望包含: '{expected_text}', 实际是: '{current_title}'"

    @allure.step("断言：检查元素 {locator} 的文本是否为 '{expected_text}'")
    def assert_text_is(self, locator, expected_text):
        """断言指定元素的文本是否完全匹配指定文本"""
        actual_text = self.get_text(locator)
        assert actual_text == expected_text, f"文本断言失败！元素: {locator}, 期望: '{expected_text}', 实际: '{actual_text}'"

 # 可根据需要扩展更多方法