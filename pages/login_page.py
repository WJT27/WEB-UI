"""
文件作用：
-----------
定义登录页面的操作与元素定位。
继承自 BasePage，实现 login() 等具体业务动作。
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    username = (By.CSS_SELECTOR, "div input[type = \"text\"]")
    password = (By.CSS_SELECTOR, "div input[type = \"password\"]")
    submit = (By.CSS_SELECTOR, "div [type = \"button\"]")

    #打开网页
    def open_url(self, url):
        self.logger.info(f"打开页面: {url}")
        self.driver.get(url)

    def login(self,user,pwd):
        self.send_keys(self.username,text = user)
        self.send_keys(self.password,text = pwd)
        self.click(self.submit)