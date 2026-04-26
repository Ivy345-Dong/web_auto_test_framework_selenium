# conftest.py
import allure
import pytest
import logging
from utility.driver_factory import DriverFactory

def pytest_addoption(parser):
    parser.addoption("--executor", action="store", default="local", help="local or grid")
    parser.addoption("--browser", action="store", default="chrome", help="chrome, firefox, edge, safari")

@pytest.fixture(scope="function")
def driver_function(request):
    executor = request.config.getoption("--executor")
    browser = request.config.getoption("--browser")
    driver = DriverFactory.get_web_driver(executor=executor, browser=browser)
    yield driver
    DriverFactory.quit_web_driver(driver)

@pytest.fixture(scope="class")
def driver_class(request):
    executor = request.config.getoption("--executor")
    browser = request.config.getoption("--browser")
    driver = DriverFactory.get_web_driver(executor=executor, browser=browser)
    yield driver
    DriverFactory.quit_web_driver(driver)

# Configure Logs
def setup_logger():
    logger = logging.getLogger('test_framework')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Console output
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
        )
        logger.addHandler(handler)

    return logger


logger = setup_logger()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically record the test execution process and failure information
    """
    # 执行测试
    outcome = yield
    report = outcome.get_result()

    # Record at the start of the test
    if report.when == "setup":
        logger.info(f"test start: {item.nodeid}")

    # record at the end of the test, if failed, record the error message
    elif report.when == "call":
        # Add Dynamic Title & Browser Tag to allure report to distinguish test results
        browser = item.config.getoption("--browser", default="unknown")
        allure.dynamic.title(f"{item.originalname} [{browser.upper()}]")
        allure.dynamic.label("browser", browser)
        allure.dynamic.tag(browser)

        #Logging test results
        if report.passed:
            logger.info(f"test passed: {item.nodeid}")
        elif report.failed:
            logger.error(f"test failed: {item.nodeid}")
            logger.error(f"error message: {call.excinfo}")

    # clean up
    elif report.when == "teardown":
        logger.info(f"test finished: {item.nodeid}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """record test setup phase"""
    logger.info(f"prepare to test: {item.name}")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    """record test teardown phase"""
    logger.info(f"clean test: {item.name}")
    yield
