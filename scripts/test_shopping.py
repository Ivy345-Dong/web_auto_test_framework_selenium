#定义测试购物袋类
import pytest

from page.cart_page import CartProxy
from page.home_page import HomeProxy
from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy
from utility.driver_factory import DriverFactory
from utility.com import is_element_present


class TestShopping:
    def setup_class(self):
        self.driver = DriverFactory.get_web_driver()
        self.home_proxy = HomeProxy()
        self.login_proxy = LoginProxy()
        self.cart_proxy = CartProxy()
        self.swag_labs_proxy = SwagLabsProxy()
        self.login_proxy.login("standard_user", "secret_sauce")

    def teardown_class(self):
        self.swag_labs_proxy.logout()
        DriverFactory.quit_web_driver()


    #test add a goods to cart
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("goods_name, count",get_json_data(r"D:\my_files\projects\saucedemo\data\test_add_to_cart.json"))
    def test_add_goods_to_cart(self, goods_name, count):
        # add a goods to cart, this method will return the number showed in cart badge
        number = self.home_proxy.add_goods_to_cart_and_check_number(goods_name)
        # assert the actual count equals expect count
        assert number == count

    #test remove from cart
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize("goods_name, count",get_json_data(r"D:\my_files\projects\saucedemo\data\test_remove_from_cart.json"))
    def test_remove_goods_from_cart(self,goods_name, count):
        self.home_proxy.home_handle.click_cart_icon()
        self.cart_proxy.remove_goods_from_cart(goods_name)
        # check the count decrease one
        assert self.home_proxy.home_handle.check_number_of_goods_in_cart() == count
        # back to home page, then can repeat this process
        self.driver.back()



