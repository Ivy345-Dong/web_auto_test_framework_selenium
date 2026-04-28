import pytest

from page.cart_page import CartProxy
from page.home_page import HomeProxy
from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy


class TestShopping:

    @pytest.fixture(scope="class", autouse=True)
    def _initialize_class(self, driver_class):
        """Initialize once for the entire test class - share browser across all tests"""
        cls = self.__class__
        cls.driver = driver_class
        cls.home_proxy = HomeProxy(driver_class)
        cls.login_proxy = LoginProxy(driver_class)
        cls.cart_proxy = CartProxy(driver_class)
        cls.swag_labs_proxy = SwagLabsProxy(driver_class)

    @pytest.mark.parametrize("goods_name1, goods_name2, add_count, left_count",
                             get_json_data(r"D:\my_files\projects\saucedemo\data\test_add_to_cart.json"))
    def test_add_goods_to_cart(self, goods_name1, goods_name2, add_count, left_count):
        #login website
        self.login_proxy.login("standard_user", "secret_sauce")
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
