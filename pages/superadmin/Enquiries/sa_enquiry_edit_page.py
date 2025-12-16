import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.common.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SAEnquiryEditPage(BasePage):

    # Status field (dynamic ID)
    STATUS = (By.NAME, 'status')
    NAME = (By.XPATH, "//div[@bp-field-name='name']")
    PHONE = (By.XPATH, "//div[@bp-field-name='contact_no_display']")
    EMAIL = (By.XPATH, "//div[@bp-field-name='business_email']")
    COMPANY = (By.XPATH, "//div[@bp-field-name='company']")
    MESSAGE = (By.XPATH, "//div[@bp-field-name='message']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'Submit') or contains(text(),'Update')]")
    SUCCESS_POPUP = (By.CSS_SELECTOR, "div.toastify")

    def wait_until_loaded(self):
        self.is_visible(self.STATUS)

    def change_status(self, value):
        dropdown = self.is_visible(self.STATUS)
        Select(dropdown).select_by_visible_text(value)
        time.sleep(0.4)  # Give UI time to enable submit button

    def click_save(self):
        self.click(self.SAVE_BUTTON)

    def wait_success(self):
        # Wait for toast message to appear
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_POPUP)
        )

        # Wait for toast message to disappear
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.SUCCESS_POPUP)
        )

    def is_submit_enabled(self):
        btn = self.driver.find_element(*self.SAVE_BUTTON)
        return btn.is_enabled()

    def get_current_status(self):
        dropdown = Select(self.driver.find_element(*self.STATUS))
        return dropdown.first_selected_option.text.strip()