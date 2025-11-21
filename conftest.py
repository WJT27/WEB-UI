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
from utils.browser_factory import create_driver
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
    # 加载配置文件config
    return load_config()


@pytest.fixture(scope="session")
def driver(config):
    """
    初始化 WebDriver，调用 browser_factory.py 进行驱动创建。
    """
    browser = config.get("browser", "chrome").lower()
    headless = config.get("headless", False)

    try:
        # **关键修改：调用外部工厂函数**
        driver = create_driver(browser=browser, headless=headless)
    except Exception as e:
        logger.error(f"浏览器驱动创建失败: {e}")
        raise

    driver.implicitly_wait(config.get("implicitly_wait", 5))
    logger.info(f"{browser} 浏览器初始化完成，headless={headless}")

    yield driver

    driver.quit()
    logger.info(f"{browser} 浏览器已关闭")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 拿到测试类实例
        page = getattr(item.instance, "page", None)
        if page:
            try:
                page.screenshot(name=report.nodeid.replace("::", "_"))
            except Exception as e:
                print(f"[截图失败]: {e}")