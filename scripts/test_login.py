#定义测试购物袋类
import pytest

from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy
from utility.driver_factory import DriverFactory
from utility.com import is_element_present


class TestLogin:
    def setup_class(self):
        self.driver = DriverFactory.get_web_driver()
        self.login_proxy = LoginProxy()
        self.swag_labs_proxy = SwagLabsProxy()

    def teardown_class(self):
        DriverFactory.quit_web_driver()

    #test login successfully
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("username, password, keywords",get_json_data(r"D:\my_files\projects\saucedemo\data\test_login.json"))
    def test_login_success(self,username, password, keywords):
        self.login_proxy.login(username, password)
        # if add to cart button exist, login success
        assert is_element_present(self.driver, keywords)
        self.swag_labs_proxy.logout()


    #test login failed
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("username, password, keywords",get_json_data(r"D:\my_files\projects\saucedemo\data\test_login_failed.json"))
    def test_login_failed(self,username, password, keywords):
        self.login_proxy.login(username, password)
        # check the error message
        assert is_element_present(self.driver, keywords)
        self.driver.refresh()


