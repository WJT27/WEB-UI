"""
文件作用：
-----------
pytest 全局配置文件。
定义 fixture（如 driver、config），
在每个测试用例运行前后自动调用。
"""
import pytest
import allure
from pathlib import Path
import os
import time

# 导入工具类
from config.config import load_config
from utils.logger import get_logger
from utils.driver_factory import DriverFactory # 导入工厂类

# 项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]
# 日志目录
LOG_DIR = BASE_DIR / "reports" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
# Logger 实例
logger = get_logger("framework")


@pytest.fixture(scope="session")
def config():
    """加载配置文件的 Fixture"""
    return load_config()


@pytest.fixture(scope="session")
def driver(config):
    """"
    初始化 WebDriver，调用 DriverFactory 进行驱动创建。
    职责：仅负责驱动的生命周期管理。
    """
    logger.info(f"开始初始化 {config['browser']} 浏览器...")

    # 使用工厂类创建驱动
    factory = DriverFactory(config)
    web_driver = factory.get_driver()

    logger.info("WebDriver 初始化完成。")

    yield web_driver

    web_driver.quit()
    logger.info("WebDriver 已关闭")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 尝试从测试实例中获取 driver
        # 注意：此处从 funcargs 中获取 driver (fixture)
        driver_fixture = item.funcargs.get("driver")

        if driver_fixture:
            config = load_config()  # 重新加载配置获取路径

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_name = f"{report.nodeid.replace('::', '_')}_{timestamp}.png"

            # 构建截图绝对路径
            screenshot_dir = BASE_DIR / config.get("screenshot_dir")
            os.makedirs(screenshot_dir, exist_ok=True)
            file_path = screenshot_dir / file_name

            # 保存截图
            driver_fixture.save_screenshot(str(file_path))
            logger.error(f"测试失败，已截图: {file_path}")

            # 附加到 Allure 报告
            with open(file_path, "rb") as f:
                allure.attach(f.read(), name="失败截图", attachment_type=allure.attachment_type.PNG)