"""
文件作用：
-----------
用于统一创建 WebDriver（浏览器）实例。
支持 Chrome 和 Firefox，可通过参数控制 headless 模式。
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.options import Options as FFOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def create_driver(browser = "chrome",headless = False):
    if browser.lower() == "chrome":
        opts =  ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--window-size=1920x1080")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
    elif browser.lower() == "firefox":
        opts = FFOptions()
        if headless:
            opts.add_argument("-headless")
        service = FFService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=opts)
    else :
        raise ValueError(f"Unsupported browser {browser}")
    return driver