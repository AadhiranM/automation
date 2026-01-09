from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker


class KYCPage(BasePage):

    # ----------- DATE PICKER -----------
    DOB = (By.ID, "dobInput")

    # ----------- INPUT FIELDS -----------
    FULL_NAME = (By.NAME, "full_name")
    DRIVING_LICENCE = (By.NAME, "driving_licence")
    PERSONAL_PAN = (By.NAME, "personal_pan")
    ADDRESS = (By.NAME, "address")
    MOBILE = (By.NAME, "mobile")

    # ----------- ERROR -----------
    ERROR_TEXT = (By.CLASS_NAME, "invalid-feedback")

    # ----------- BUTTON -----------
    NEXT_BTN = (By.XPATH, "//button[normalize-space()='Next']")

    # ----------- PAGE MARKER -----------
    PAGE_MARKER = (By.XPATH, "//h5[contains(text(),'KYC Verification')]")

    # ================= PAGE LOAD =================

    def wait_for_page(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.DOB)
        )

    # ================= FIELD ACTIONS =================

    def fill_dob(self, date_str):
        dob_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DOB)
        )
        dob_input.click()
        picker = FlatpickrRangePicker(self.driver)
        picker.select_single_date_static(date_str)

    def fill_full_name(self, name):
        self.type(self.FULL_NAME, name)

    def fill_driving_licence(self, licence):
        self.type(self.DRIVING_LICENCE, licence)

    def fill_personal_pan(self, pan):
        self.type(self.PERSONAL_PAN, pan)

    def fill_address(self, address):
        self.type(self.ADDRESS, address)

    def fill_mobile(self, mobile):
        self.type(self.MOBILE, mobile)

    # ================= ALIAS METHODS (FOR TEST READABILITY) =================
    # ✅ These fix your unresolved errors

    def fill_director_name(self, name):
        self.fill_full_name(name)

    def fill_director_pan(self, pan):
        self.fill_personal_pan(pan)

    def fill_director_driving_license(self, DL):
        self.type(self.DRIVING_LICENCE, DL)  # if aadhar field exists later, update locator

    def select_director_dob(self, date):
        self.fill_dob(date)

    # ================= ACTION =================

    def click_next(self):
        self.click(self.NEXT_BTN)

    # ================= VALIDATION =================

    def is_error_visible(self):
        return len(self.driver.find_elements(*self.ERROR_TEXT)) > 0
