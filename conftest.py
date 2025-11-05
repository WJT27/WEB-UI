"""
文件作用：
-----------
pytest 全局配置文件。
定义 fixture（如 driver、config），
在每个测试用例运行前后自动调用。
"""
import pytest
from selenium import webdriver

from utils.browser_factory import create_driver
from utils.config import load_config

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture
def driver(config,request):
    browser = config["browser"]
    headless = config["headless"]
    d = create_driver(browser,headless)
    d.implicitly_wait(config.get("implicit_wait",5))
    yield d
    #如果测试失败,截图保存
    if request.node.rep_call.failed:
        d.save_screenshot("failure.png")
    d.quit()

# pytest hook：用于让 driver fixture 知道测试结果（passed/failed）
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)