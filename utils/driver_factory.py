# utils/driver_factory.py (浏览器驱动工厂类)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FFService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverFactory:
    """负责根据配置创建和配置 WebDriver 实例的工厂类"""

    def __init__(self, config):
        self.config = config
        self.browser = config.get("browser", "chrome").lower()
        self.headless = config.get("headless", False)

    def get_driver(self):
        """根据配置返回 WebDriver 实例"""
        driver = None
        
        if self.browser == "chrome":
            driver = self._create_chrome()
        elif self.browser == "firefox":
            driver = self._create_firefox()
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser}")

        # 统一设置隐式等待
        driver.implicitly_wait(self.config.get("implicitly_wait", 10))
        return driver

    def _create_chrome(self):
        """创建 Chrome 驱动实例"""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3") 
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _create_firefox(self):
        """创建 Firefox 驱动实例"""
        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument("-headless")
        
        service = FFService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)