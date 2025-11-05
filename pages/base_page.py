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
        self.logger = get_logger(self.__class__.__name__)  # 每个页面有独立 logger


    #查找元素
    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    #点击元素
    def click(self, locator):
        self.logger.info(f"点击元素")
        el = self.find_element(locator)
        el.click()

    #输入内容
    def send_keys(self, locator, text):
        self.logger.info(f"输入内容: {text} ")
        el = self.find_element(locator)
        el.clear()
        el.send_keys(text)

    #获取标题
    def get_title(self):
        return self.driver.title

    #获取文本
    def get_text(self,locator):
        text = self.driver.find(locator).text
        self.logger.info(f"获取文本: {text}")
        return text

 # 可根据需要扩展更多方法