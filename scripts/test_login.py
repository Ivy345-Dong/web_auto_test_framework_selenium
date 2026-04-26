# 定义测试登录类
import pytest

from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy
from utility.driver_factory import DriverFactory
from utility.com import is_element_present


class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """为每个测试方法创建独立的浏览器实例"""
        # 打开浏览器
        self.driver = DriverFactory.get_web_driver()
        self.login_proxy = LoginProxy()
        self.swag_labs_proxy = SwagLabsProxy()

        yield

        # 关闭浏览器
        DriverFactory.quit_web_driver()

    # test login successfully
    @pytest.mark.parametrize("username, password, keywords",
                             get_json_data(r"D:\my_files\projects\saucedemo\data\test_login.json"))
    def test_login_success(self, username, password, keywords):
        """Test successful login - runs with fresh browser"""
        self.login_proxy.login(username, password)
        # if add to cart button exist, login success
        assert is_element_present(self.driver, keywords)
        self.swag_labs_proxy.logout()

    # test login failed
    @pytest.mark.parametrize("username, password, keywords",
                             get_json_data(r"D:\my_files\projects\saucedemo\data\test_login_failed.json"))
    def test_login_failed(self, username, password, keywords):
        """Test failed login - runs with fresh browser"""
        self.login_proxy.login(username, password)
        # check the error message
        assert is_element_present(self.driver, keywords)
        self.driver.refresh()
