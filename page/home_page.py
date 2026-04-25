#首页页面对象
import time
import allure
from selenium.webdriver.common.by import By
from base.base import BasePage, BaseHandle


#define locators class
class HomePage(BasePage):
    """Page object for Home page"""

    #Locators
    # add to cart button
    ADD_TO_CART_BUTTON = By.CSS_SELECTOR, "[data-test='add-to-cart-{}']"
    # cart icon
    CART_ICON = By.CSS_SELECTOR, "[data-test='shopping-cart-link']"
    # cart badge that can show the number of the goods in cart
    CART_BADGE = By.CSS_SELECTOR, "[data-test='shopping-cart-badge']"

    def __init__(self):
        super().__init__()


    # add to cart button
    def find_add_to_cart_button(self, goods_name):
        goods_name_changed = goods_name.lower().replace(" ", "-")
        locator = self.ADD_TO_CART_BUTTON[0], self.ADD_TO_CART_BUTTON[1].format(goods_name_changed)
        return self.get_element(locator)

    # find cart icon
    def find_cart_icon(self):
        return self.get_element(self.CART_ICON)

    # find cart badge
    def find_cart_badge(self):
        return self.get_element(self.CART_BADGE)


#define operations class
class HomeHandle(BaseHandle):
    def __init__(self):
        self.home_page = HomePage()

    @allure.step(title="choose a goods and add to cart")
    def add_to_cart_with_goods_name(self, goods_name):
        self.home_page.find_add_to_cart_button(goods_name).click()

    @allure.step(title="obtain the number of goods in cart")
    def check_number_of_goods_in_cart(self):
        number = self.home_page.find_cart_badge().text
        return number

    @allure.step(title="go the the cart page")
    def click_cart_icon(self):
        self.home_page.find_cart_icon().click()


#define business actions
class HomeProxy:
    def __init__(self):
        self.home_handle = HomeHandle()

    @allure.step(title="add goods to cart and check number")
    def add_goods_to_cart_and_check_number(self, goods_name):
        self.home_handle.add_to_cart_with_goods_name(goods_name)
        #wait for the cart badge updating number
        time.sleep(2)
        return self.home_handle.check_number_of_goods_in_cart()

