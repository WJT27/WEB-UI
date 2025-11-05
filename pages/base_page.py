"""
文件作用：
-----------
BasePage 封装所有页面通用的 Selenium 操作：
包括 find 元素、click、type、visit 等。
其他页面类继承它，实现自己的业务逻辑。
"""
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url):
        self.logger.info(f"打开网页: {url}")
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.logger.info(f"点击元素: {by}={locator}")
        el = self.find(locator)
        el.click()

    def send_keys(self, locator, text):
        self.logger.info(f"输入内容: {text} -> {by}={locator}")
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def getTitle(self):
        return self.driver.title

    def get_text(self,locator):
        text = self.driver.find(locator).text
        self.logger.info(f"获取文本: {text}")
        return text

    def quit(self):
        self.driver.quit()