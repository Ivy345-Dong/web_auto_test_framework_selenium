import pytest

from page.cart_page import CartProxy
from page.home_page import HomeProxy
from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy
from utility.driver_factory import DriverFactory
from utility.com import is_element_present


@pytest.mark.usefixtures("driver_class")
class TestShopping:

    @classmethod
    def setup_class(cls):
        """Initialize page objects before all tests"""
        cls.driver = DriverFactory.get_web_driver()
        cls.home_proxy = HomeProxy()
        cls.login_proxy = LoginProxy()
        cls.cart_proxy = CartProxy()
        cls.swag_labs_proxy = SwagLabsProxy()

    # Step 1: Login
    def test_login(self):
        """Test login to the application"""
        self.login_proxy.login("standard_user", "secret_sauce")

    # Step 2: Test add goods to cart
    @pytest.mark.parametrize("goods_name, count",
                             get_json_data(r"D:\my_files\projects\saucedemo\data\test_add_to_cart.json"))
    def test_add_goods_to_cart(self, goods_name, count):
        """Test adding goods to cart - runs after login"""
        number = self.home_proxy.add_goods_to_cart_and_check_number(goods_name)
        assert number == count

    # Step 3: Test remove goods from cart
    @pytest.mark.parametrize("goods_name, count",
                             get_json_data(r"D:\my_files\projects\saucedemo\data\test_remove_from_cart.json"))
    def test_remove_goods_from_cart(self, goods_name, count):
        """Test removing goods from cart - runs after add test"""
        self.home_proxy.home_handle.click_cart_icon()
        self.cart_proxy.remove_goods_from_cart(goods_name)
        assert self.home_proxy.home_handle.check_number_of_goods_in_cart() == count
        self.driver.back()

    # Step 4: Logout
    def test_logout(self):
        """Test logout from the application"""
        self.swag_labs_proxy.logout()
