import time

import allure
from selenium.webdriver.common.by import By

from base.base import BasePage, BaseHandle


#define locators class
class SwagLabs(BasePage):
    """Page object for Swag Labs"""

    #Locators
    # menu button
    MENU_BUTTON = By.CSS_SELECTOR, "#react-burger-menu-btn"
    #logout button
    LOGOUT_BUTTON = By.CSS_SELECTOR, "#logout_sidebar_link"

    def __init__(self, driver=None):
        super().__init__(driver)

    def find_menu_button(self):
        return self.get_element(self.MENU_BUTTON)

    def find_logout_button(self):
        return self.get_element(self.LOGOUT_BUTTON)


#define operations class
class SwagLabsHandle(BaseHandle):
    def __init__(self, driver=None):
        self.swag_labs_page = SwagLabs(driver)

    @allure.step(title="click menu button")
    def click_menu_button(self):
        self.swag_labs_page.find_menu_button().click()

    @allure.step(title="click logout button")
    def click_logout_button(self):
        self.swag_labs_page.find_logout_button().click()


#define business actions
class SwagLabsProxy:
    def __init__(self, driver=None):
        self.swag_labs_handle = SwagLabsHandle(driver)

    @allure.step(title="logout from swag labs")
    def logout(self):
        self.swag_labs_handle.click_menu_button()
        time.sleep(2)
        self.swag_labs_handle.click_logout_button()