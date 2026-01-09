from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage
import datetime
import time
from utilities.flatpickr import FlatpickrRangePicker

class BusinessInfoPage(BasePage):
    """
    Page Object for Manufacturer Onboarding - Business Information step
    Supports Select2 dropdowns (scroll + search)
    """

    # ---------- FORM ----------
    FORM = (By.ID, "business_info_form")

    # ---------- INPUT FIELDS ----------
    COMPANY_NAME = (By.ID, "companyNameInput")
    BUSINESS_EMAIL = (By.NAME, "business_email")
    GST_NUMBER = (By.NAME, "gst_no")
    BUSINESS_PAN_NUMBER = (By.NAME, "pan_no")
    WEBSITE = (By.NAME, "website_url")

    # ---------- SELECT2 DROPDOWNS ----------
    BUSINESS_TYPE_DROPDOWN = (
        By.XPATH, "//span[contains(@id,'select2-business_type_id-container')]"
    )

    INDUSTRY_DROPDOWN = (
        By.XPATH, "//span[contains(@id,'select2-industry_type_id-container')]"
    )

    SELECT2_SEARCH_INPUT = (
        By.XPATH, "//input[contains(@class,'select2-search__field')]"
    )

    SELECT2_OPTIONS = (
        By.XPATH, "//li[contains(@class,'select2-results__option')]"
    )

    # ---------- NORMAL DROPDOWN ----------
    ANNUAL_TURNOVER = (By.ID, "annual_turnover")

    # ---------- BUTTON ----------
    NEXT_BTN = (By.XPATH, "//button[normalize-space()='Next']")

    # ---------- VALIDATION ----------
    ERROR_MSG = (
        By.XPATH, "//div[contains(@class,'invalid-feedback') or contains(@class,'error-msg')]"
    )

    DATE_OF_INCORPORATION = (
        By.XPATH,
        "//input[contains(@class,'flatpickr-input') and @placeholder='DD-MM-YYYY']"
    )

    # ---------- PAGE LOAD ----------
    def wait_for_page(self):
        """
        Business Info page is ready when Company Name input is visible
        """
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.COMPANY_NAME)
        )

    # ---------- INPUT ACTIONS ----------
    def fill_company_name(self, name):
        self.type(self.COMPANY_NAME, name)

    def fill_business_email(self, email):
        self.type(self.BUSINESS_EMAIL, email)

    def fill_date_of_incorporation(self, date_str):
        """
        Set Date of Incorporation using Flatpickr internal API
        date_str format: DD-MM-YYYY
        """

        date_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.DATE_OF_INCORPORATION)
        )

        # Scroll to input (important)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            date_input
        )

        # Set date via flatpickr instance (THIS IS THE FIX)
        self.driver.execute_script("""
            if (arguments[0]._flatpickr) {
                arguments[0]._flatpickr.setDate(arguments[1], true, "d-m-Y");
            } else {
                throw "Flatpickr instance not found";
            }
        """, date_input, date_str)

    def fill_gst(self, gst):
        self.type(self.GST_NUMBER, gst)

    def fill_pan(self, pan):
        self.type(self.BUSINESS_PAN_NUMBER, pan)

    def fill_website(self, url):
        self.type(self.WEBSITE, url)

    # =====================================================
    # SELECT2 HANDLERS (BEST PRACTICE)
    # =====================================================

    def open_select2_and_wait_for_options(self, dropdown):
        self.click(dropdown)
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.SELECT2_OPTIONS)
        )

    def select_select2_option_by_typing(self, dropdown, option_text):
        """
        Use when exact option is required
        """
        self.open_select2_and_wait_for_options(dropdown)

        search = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.SELECT2_SEARCH_INPUT)
        )
        search.clear()
        search.send_keys(option_text)
        search.send_keys(Keys.ENTER)

    def select_first_available_select2_option(self, dropdown):
        """
        Use when user scrolls and selects any option
        """
        self.open_select2_and_wait_for_options(dropdown)

        options = self.driver.find_elements(*self.SELECT2_OPTIONS)
        for option in options:
            if "disabled" not in option.get_attribute("class"):
                option.click()
                break

    # ---------- BUSINESS TYPE ----------
    def select_business_type(self, value=None):
        if value:
            self.select_select2_option_by_typing(self.BUSINESS_TYPE_DROPDOWN, value)
        else:
            self.select_first_available_select2_option(self.BUSINESS_TYPE_DROPDOWN)

    # ---------- INDUSTRY ----------
    def select_industry(self, value=None):
        if value:
            self.select_select2_option_by_typing(self.INDUSTRY_DROPDOWN, value)
        else:
            self.select_first_available_select2_option(self.INDUSTRY_DROPDOWN)

    # ---------- ANNUAL TURNOVER ----------
    def select_annual_turnover(self, value):
        self.select_by_visible_text(self.ANNUAL_TURNOVER, value)

    # ---------- NEXT ----------
    def click_next(self):
        self.click(self.NEXT_BTN)

    # ---------- VALIDATION ----------
    def is_error_visible(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.ERROR_MSG)
            )
            return True
        except:
            return False

    def goto_page(self):
        """
        Navigate to Manufacturer Onboarding - Business Info page
        """
        self.driver.get(
            "https://beta.digitathya.com/admin/manufacturer/onboarding"
        )


