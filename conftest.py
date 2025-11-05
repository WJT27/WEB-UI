"""
文件作用：
-----------
pytest 全局配置文件。
定义 fixture（如 driver、config），
在每个测试用例运行前后自动调用。
"""
import pytest
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure

# 导入你的配置模块和日志工具
from config.config import load_config
from utils.logger import get_logger

# 项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]

# 日志目录
LOG_DIR = BASE_DIR / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logger 实例
logger = get_logger("framework")


@pytest.fixture(scope="session")
def config():
    """
    加载测试框架配置
    """
    cfg = load_config()
    logger.info(f"加载配置：{cfg}")
    return cfg


@pytest.fixture(scope="session")
def driver(config):
    """
    初始化 WebDriver
    """
    browser = config.get("browser", "chrome").lower()
    headless = config.get("headless", False)

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        driver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=driver_service, options=options)
    else:
        raise Exception(f"浏览器 {browser} 不支持")

    driver.implicitly_wait(config.get("implicitly_wait", 5))
    logger.info(f"{browser} 浏览器初始化完成，headless={headless}")
    yield driver
    driver.quit()
    logger.info(f"{browser} 浏览器已关闭")


# 自动失败截图并附加到 Allure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 只在测试用例执行阶段失败时触发
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                screenshot_name = f"{item.name}_{datetime.now():%Y%m%d%H%M%S}.png"
                screenshot_path = LOG_DIR / screenshot_name
                driver.save_screenshot(str(screenshot_path))
                logger.error(f"用例失败，截图保存至：{screenshot_path}")
                allure.attach.file(str(screenshot_path), name="失败截图", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                logger.error(f"截图失败: {e}")
