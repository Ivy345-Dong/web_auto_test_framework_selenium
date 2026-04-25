# conftest.py
import pytest
import logging


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
