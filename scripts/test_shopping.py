import pytest

from page.cart_page import CartProxy
from page.home_page import HomeProxy
from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy


class TestShopping:

    @pytest.fixture(autouse=True)
    def setup_method(self, driver_function):
        """Create independent browser instance for each test method"""
        self.driver = driver_function
        self.home_proxy = HomeProxy(self.driver)
        self.login_proxy = LoginProxy(self.driver)
        self.swag_labs_proxy = SwagLabsProxy(self.driver)
        self.cart_proxy = CartProxy(self.driver)



    @pytest.mark.parametrize("username, password, goods_name1, goods_name2, add_count, left_count",
                             get_json_data("./data/test_add_to_cart.json"))
    def test_add_goods_to_cart(self, username, password, goods_name1, goods_name2, add_count, left_count):
        # login website
        self.login_proxy.login(username, password)
        #add 2 goods to cart and check number
        self.home_proxy.add_goods_to_cart_and_check_number(goods_name1)
        number = self.home_proxy.add_goods_to_cart_and_check_number(goods_name2)
        assert number == add_count
        #go to cart page and remove one from cart
        self.home_proxy.home_handle.click_cart_icon()
        self.cart_proxy.remove_goods_from_cart(goods_name1)
        assert self.home_proxy.home_handle.check_number_of_goods_in_cart() == left_count
        #logout
        self.swag_labs_proxy.logout()
