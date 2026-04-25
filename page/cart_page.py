#唯品会web首页页面对象
import time

import allure
from selenium.webdriver.common.by import By

from base.base import BasePage, BaseHandle


#define locators class
class CartPage(BasePage):
    """Page object for Cart page"""

    #Locators
    # remove button
    REOMVE_BUTTON = By.CSS_SELECTOR, "[data-test='remove-{}']"

    def __init__(self):
        super().__init__()


    # add to cart button
    def find_remove_button(self, goods_name):
        goods_name_changed = goods_name.lower().replace(" ", "-")
        locator = self.REOMVE_BUTTON[0], self.REOMVE_BUTTON[1].format(goods_name_changed)
        return self.get_element(locator)



#define operations class
class CartHandle(BaseHandle):
    def __init__(self):
        self.cart_page = CartPage()

    @allure.step(title="choose a goods and remove from cart")
    def remove_from_cart_with_goods_name(self, goods_name):
        self.cart_page.find_remove_button(goods_name).click()


#define business actions
class CartProxy:
    def __init__(self):
        self.cart_handle = CartHandle()

    @allure.step(title="remove goods from cart and check number")
    def remove_goods_from_cart(self, goods_name):
        self.cart_handle.remove_from_cart_with_goods_name(goods_name)
        #wait for the cart badge updating number
        time.sleep(2)


