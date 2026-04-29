import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Encapsulate a method to check if an element exists
def is_element_present(driver, text, timeout=10):
    """
    Check if an element with the given text exists on the page.
    Uses explicit wait for stability, captures screenshot on failure.
    """
    xpath = f"//*[contains(text(), '{text}')]"
    try:
        # ✅ Use explicit wait instead of hard sleep
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return True
    except Exception as e:
        # ✅ Attach screenshot only on failure
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"Element '{text}' not found",
            attachment_type=allure.attachment_type.PNG
        )
        return False