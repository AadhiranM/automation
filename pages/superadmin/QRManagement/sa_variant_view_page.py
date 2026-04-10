from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker

class SAVariantViewPage(BasePage):

    MANUFACTURER = (By.ID, "manufacturer_id")
    CATEGORY = (By.ID, "category_id")

    def are_fields_disabled(self):
        manufacturer = self.get_element(self.MANUFACTURER)
        category = self.get_element(self.CATEGORY)

        return (
                manufacturer.get_attribute("disabled")
                or manufacturer.get_attribute("readonly")
        ) and (
                category.get_attribute("disabled")
                or category.get_attribute("readonly")
        )