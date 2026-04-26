import pytest

from page.cart_page import CartProxy
from page.home_page import HomeProxy
from page.swag_labs import SwagLabsProxy
from utility.data_reader import get_json_data
from page.login_page import LoginProxy
from utility.driver_factory import DriverFactory
from utility.com import is_element_present


class TestShopping:

    @pytest.fixture(scope="class", autouse=True)
    def _initialize_class(self, driver_class):
        """Initialize once for the entire test class - share browser across all tests"""
        # 使用 cls 设置类属性，保持一致性
        cls = self.__class__
        cls.driver = driver_class
        cls.home_proxy = HomeProxy(driver_class)
        cls.login_proxy = LoginProxy(driver_class)
        cls.cart_proxy = CartProxy(driver_class)
        cls.swag_labs_proxy = SwagLabsProxy(driver_class)

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
