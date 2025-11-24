"""
文件作用：
-----------
定义登录页面的操作与元素定位。
继承自 BasePage，实现 login() 等具体业务动作。
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    # --- 元素定位器 ---
    USERNAME = (By.CSS_SELECTOR, "div input[type = \"text\"]")
    PASSWORD = (By.CSS_SELECTOR, "div input[type = \"password\"]")
    SUBMIT = (By.CSS_SELECTOR, "div [type = \"button\"]")

    #打开网页
    def login(self,username,password):
        self.visit("")
        self.send_keys(self.USERNAME,text = username)
        self.send_keys(self.PASSWORD,text = password)
        self.click(self.SUBMIT)

    # def get_Login_error(self,locator):
        # 使用 BasePage 的方法获取文本
        # return self.get_text(self.ERROR_MESSAGE)