from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccessCodePage:
    ACCESS_CODE_INPUT = (By.NAME, "access_code")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")  # Update if needed

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    def enter_access_code(self, code):
        try:
            access_code_input = self.wait.until(
                EC.visibility_of_element_located(self.ACCESS_CODE_INPUT)
            )
            access_code_input.click()
            access_code_input.send_keys(code)
            self.driver.find_element(*self.SUBMIT_BUTTON).click()
            return True
        except Exception:
            # Access code page not present
            return False
