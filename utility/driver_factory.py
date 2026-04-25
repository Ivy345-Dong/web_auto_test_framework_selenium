#define driver class
import os
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utility.data_reader import get_env_url


class DriverFactory:
    _web_driver = None #Define the browser driver
    _remote_driver = None
    _logger = logging.getLogger('test_framework')

    #Define the browser driver for accessing web pages
    @classmethod
    def get_web_driver(cls):
        if cls._web_driver is None:
            # initialize driver
            options = Options()
            # Core speed fixes
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-sync")
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--disable-client-side-phishing-detection")
            options.add_argument("--disable-component-update")
            options.add_argument("--safebrowsing-disable-auto-update")
            options.add_argument("--disable-web-security")
            options.add_argument("--disk-cache-size=1073741824")  # 1GB cache
            options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
            options.add_argument("--incognito")
            options.add_argument("--safebrowsing-disable-download-protection")
            options.add_argument("--safebrowsing-disable-extension-blacklist")
            options.add_argument("--headless=new")
            cls._web_driver = webdriver.Chrome(options=options)
            cls._web_driver.maximize_window()
            # open the url
            cls._web_driver.get(get_env_url())
        return cls._web_driver

    #Define the browser driver for exiting the web page
    @classmethod
    def quit_web_driver(cls):
        if cls._web_driver is not None:
            cls._web_driver.quit()
            cls._web_driver = None
            cls._kill_chromedriver_only()

    @classmethod
    def _kill_chromedriver_only(cls):
        """Only clean up the chromedriver processes without affecting chrome.exe."""
        if os.name == 'nt':  # Windows
            try:
                subprocess.call('taskkill /F /IM chromedriver.exe /T',
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
            except Exception:
                pass
        else:  # Linux/Mac
            try:
                subprocess.call(['pkill', '-f', 'chromedriver'])
            except Exception:
                pass


