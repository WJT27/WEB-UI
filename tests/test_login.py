# tests/test_login.py
import pytest
import allure
from pages.login_page import LoginPage
from config.config import load_data

# 加载测试数据
test_data = load_data("test_login_data.yaml")

# 使用 Pytest 参数化 (数据驱动)
@pytest.mark.parametrize("case", test_data["valid_login_cases"])
@allure.feature("登录功能")
class TestLoginSuccess:

    # 自动注入 driver Fixture
    def test_login_success(self, driver, case):
        allure.dynamic.title(case["description"])

        login_page = LoginPage(driver)

        # 执行操作
        login_page.login(case["username"], case["password"])

        # 使用 BasePage 中的断言方法
        login_page.assert_title_contains(case["expected_title"])

@pytest.mark.parametrize("case", test_data["invalid_login_cases"])
@allure.feature("登录功能")
class TestLoginFailure:

    def test_login_failure(self, driver, case):
        allure.dynamic.title(case["description"])

        login_page = LoginPage(driver)

        # 执行操作
        login_page.login(case["username"], case["password"])

        # 使用 BasePage 中的断言方法
        login_page.assert_text_is(login_page.ERROR_MESSAGE, case["expected_error_message"])