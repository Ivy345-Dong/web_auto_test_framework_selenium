#define driver class
import os
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from utility.data_reader import get_env_url


class DriverFactory:
    _logger = logging.getLogger('test_framework')

    #Define the browser driver for accessing web pages
    @classmethod
    def get_web_driver(cls, executor="local", browser="chrome", grid_url="http://localhost:4444/wd/hub"):
        if executor == "local":
            if browser == "chrome":
                options = ChromeOptions()
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
                options.add_argument("--disk-cache-size=1073741824")
                options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
                options.add_argument("--incognito")
                options.add_argument("--safebrowsing-disable-download-protection")
                options.add_argument("--safebrowsing-disable-extension-blacklist")
                driver = webdriver.Chrome(options=options)
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)
            elif browser == "edge":
                options = EdgeOptions()
                #options.add_argument("--headless")
                driver = webdriver.Edge(options=options)
            elif browser == "safari":
                options = SafariOptions()
                driver = webdriver.Safari(options=options)
            else:
                raise ValueError(f"Unsupported browser: {browser}")
        elif executor == "grid":
            if browser == "chrome":
                options = ChromeOptions()
                #options.add_argument("--headless=new")
                driver = webdriver.Remote(command_executor=grid_url, options=options)
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                driver = webdriver.Remote(command_executor=grid_url, options=options)
            elif browser == "edge":
                options = EdgeOptions()
                options.add_argument("--headless")
                driver = webdriver.Remote(command_executor=grid_url, options=options)
            elif browser == "safari":
                options = SafariOptions()
                driver = webdriver.Remote(command_executor=grid_url, options=options)
            else:
                raise ValueError(f"Unsupported browser: {browser}")
        else:
            raise ValueError(f"Unsupported executor: {executor}")

        driver.maximize_window()
        driver.get(get_env_url())
        return driver

    #Define the browser driver for exiting the web page
    @classmethod
    def quit_web_driver(cls, driver):
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                cls._logger.warning(f"Error quitting driver: {e}")
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


