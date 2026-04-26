import allure
from selenium.webdriver.common.by import By

from base.base import BasePage, BaseHandle


#define locators class
class LoginPage(BasePage):
    """Page object for Login page"""

    #Locators
    # username input
    USERNAME_INPUT = By.CSS_SELECTOR, "#user-name"
    # password input
    PASSWORD_INPUT = By.CSS_SELECTOR, "#password"
    # login button
    LOGIN_BUTTON = By.CSS_SELECTOR, "#login-button"

    def __init__(self, driver=None):
        super().__init__(driver)


    # find username input
    def find_unsername_input(self):
        return self.get_element(self.USERNAME_INPUT)

    # find password input
    def find_password_input(self):
        return self.get_element(self.PASSWORD_INPUT)

    def find_login_button(self):
        return self.get_element(self.LOGIN_BUTTON)


#define operations class
class LoginHandle(BaseHandle):
    def __init__(self, driver=None):
        self.login_page = LoginPage(driver)

    @allure.step(title="input username")
    def input_username(self, username):
        self.input_text(self.login_page.find_unsername_input(), username)

    @allure.step(title="input password")
    def input_password(self, password):
        self.input_text(self.login_page.find_password_input(), password)

    @allure.step(title="click login button")
    def click_login_button(self):
        self.login_page.find_login_button().click()


##define business actions
class LoginProxy:
    def __init__(self, driver=None):
        self.login_handle = LoginHandle(driver)

    @allure.step(title="login with username and password")
    def login(self, username, password):
        self.login_handle.input_username(username)
        self.login_handle.input_password(password)
        self.login_handle.click_login_button()
