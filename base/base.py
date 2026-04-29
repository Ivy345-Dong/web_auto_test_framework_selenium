# Define base class for web testing
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from utility.driver_factory import DriverFactory


class BasePage:
    def __init__(self, driver=None):
        self.driver = driver if driver else DriverFactory.get_web_driver()

    def get_element(self, location):
        wait = WebDriverWait(self.driver,10,1)
        element = wait.until(EC.presence_of_element_located(location))
        return element

    # Mouse hover element
    def stay_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element)  # Move mouse to specified element and hover
        action.perform()  # Execute hover operation
        time.sleep(3)

class BaseHandle:


    def __init__(self, driver=None):
        self.base_page = BasePage(driver)

    # Input text
    # define a method to input text
    def input_text(self, element, text):
        element.clear() # Clear input field
        element.send_keys(text)
        time.sleep(1)

    '''
    # 定义一个web浏览器的边滚动边查找
    def web_scroll_find(self, direct, location):
        """

        :param driver: web浏览器驱动对象
        :param direct: 滚动方向：down, right
        :param element: 要查找的元素
        :return:
        """
        size = self.driver.get_window_size()
        while True:
            page_source = self.driver.page_source
            try:
                #call get_element() to find element
                self.get_element(location)
            except Exception as e:
                if direct == "down":
                    js = "window.scrollTo({}, {})".format(0, size["height"] * 0.3)
                    self.driver.execute_script(js)
                else:
                    js = "window.scrollTo({}, {})".format(size["width"] * 0.5, 0)
                    self.driver.execute_script(js)
            if page_source == self.driver.page_source:
                print("can not find element")
                allure.attach(self.driver.get_screenshot_as_png(), "没有找到元素截图", allure.attachment_type.PNG)
                return False
    '''
    # Switch window
    def change_window(self, handle):
        """

        :param driver: web浏览器驱动
        :param handle: 想要切换的窗口句柄：0：原窗口； -1：最后一个窗口
        :return:
        """
        time.sleep(2)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[handle])
        time.sleep(2)