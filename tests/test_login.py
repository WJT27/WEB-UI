"""
文件作用：
-----------
示例测试文件，展示如何调用 Page Object。
使用 pytest.mark.parametrize 实现数据驱动。
"""
import pytest
from pages.login_page import LoginPage


@pytest.mark.parametrize("user,pwd",[
    ("testUser01", "Lcdp!123456"),
])
def test_login(driver,config,user,pwd):
    lp = LoginPage(driver)
    lp.open(config["base_url"])
    lp.login(user,pwd)