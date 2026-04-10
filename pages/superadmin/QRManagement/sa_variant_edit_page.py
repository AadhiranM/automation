from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker

class SAVariantEditPage(BasePage):

    VARIANT_VALUE_INPUT = (By.XPATH, "(//input[@placeholder='Enter Variant Value'])[1]")
    UPDATE_BUTTON = (By.XPATH, "//button[contains(text(),'Update Variant')]")

    TOAST = (By.XPATH, "//div[contains(@class,'toastify')]")

    def update_variant_value(self, value):
        self.send_keys(self.VARIANT_VALUE_INPUT, value)

    def click_update(self):
        self.click(self.UPDATE_BUTTON)

    def get_toast(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.TOAST)).text