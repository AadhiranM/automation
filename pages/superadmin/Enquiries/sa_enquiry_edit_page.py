from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.common.base_page import BasePage

class SAEnquiryEditPage(BasePage):

    # Enabled field
    STATUS = (By.XPATH, "//select[@id='edit-status']")

    # Disabled read-only fields
    NAME = (By.XPATH, "//div[@bp-field-name='name']")
    PHONE = (By.XPATH, "//div[@bp-field-name='contact_no_display']")
    EMAIL = (By.XPATH, "//div[@bp-field-name='business_email']")
    COMPANY = (By.XPATH, "//div[@bp-field-name='company']")
    MESSAGE = (By.XPATH, "//div[@bp-field-name='message']")

    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Update' or normalize-space()='Submit']")

    # POPUP
    SUCCESS_POPUP = (By.XPATH, "//div[contains(@id,'swal2-html') and contains(text(),'updated')]")
    SUCCESS_OK = (By.XPATH, "//button[contains(@class,'swal2-confirm')]")

    def change_status(self, value):
        """Select any status from dropdown."""
        dropdown = self.is_visible(self.STATUS)
        Select(dropdown).select_by_visible_text(value)

    def click_save(self):
        self.click(self.SAVE_BUTTON)

    def wait_success(self):
        self.is_visible(self.SUCCESS_POPUP)
        self.click(self.SUCCESS_OK)

    def is_submit_enabled(self):
        """Returns True if Update/Submit button is enabled."""
        btn = self.driver.find_element(*self.SAVE_BUTTON)
        return btn.is_enabled()

    def get_current_status(self):
        """Return selected status from dropdown."""
        dropdown = Select(self.driver.find_element(*self.STATUS))
        return dropdown.first_selected_option.text.strip()