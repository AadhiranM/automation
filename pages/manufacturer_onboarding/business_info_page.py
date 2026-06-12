from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage
import time


class BusinessInfoPage(BasePage):

    COMPANY_NAME = (By.ID, "companyNameInput")
    BUSINESS_EMAIL = (By.NAME, "business_email")

    NEXT_BTN = (
        By.XPATH,
        "//button[normalize-space()='Continue to KYC Verification']"
    )

    ERROR_MSG = (
        By.XPATH,
        "//div[contains(@class,'invalid-feedback')]"
    )

    GST = (By.NAME, "gst_no")
    PAN = (By.NAME, "pan_no")
    WEBSITE = (By.NAME, "website_url")

    DATE_OF_INCORP = (
        By.XPATH,
        "//input[contains(@class,'flatpickr-input') and @placeholder='DD-MM-YYYY']"
    )

    BUSINESS_TYPE = (By.XPATH, "//span[contains(@id,'select2-business_type_id-container')]")

    INDUSTRY = (By.XPATH, "//span[contains(@id,'select2-industry_type_id-container')]")
    SELECT2_INPUT = (By.CLASS_NAME, "select2-search__field")

    ANNUAL_TURNOVER = (
        By.XPATH,
        "//span[@id='select2-annual_turnover-container']"
    )

    # =====================================================
    # PAGE LOAD
    # =====================================================

    def wait_for_page(self):

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                self.COMPANY_NAME
            )
        )

    def goto_page(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/manufacturer/onboarding"
        )

    # =====================================================
    # FIELDS
    # =====================================================

    def fill_company_name(self, name):

        self.type(
            self.COMPANY_NAME,
            name
        )

    def fill_business_email(self, email):

        self.type(
            self.BUSINESS_EMAIL,
            email
        )

    def fill_date_of_incorporation(self, date_str):

        el = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.DATE_OF_INCORP
            )
        )

        self.driver.execute_script(
            "arguments[0]._flatpickr.setDate(arguments[1], true);",
            el,
            date_str
        )

    def fill_gst(self, gst):

        self.type(
            self.GST,
            gst
        )

    def fill_pan(self, pan):

        self.type(
            self.PAN,
            pan
        )

    def fill_website(self, url):

        self.type(
            self.WEBSITE,
            url
        )

    # =====================================================
    # CHOICE.JS DROPDOWNS
    # =====================================================

    def select_business_type(self):

        self.click(
            self.BUSINESS_TYPE
        )

        active = self.driver.switch_to.active_element

        active.send_keys(
            Keys.ARROW_DOWN
        )

        active.send_keys(
            Keys.ENTER
        )

    def select_industry(self):

        self.click(
            self.INDUSTRY
        )

        active = self.driver.switch_to.active_element

        active.send_keys(
            Keys.ARROW_DOWN
        )

        active.send_keys(
            Keys.ENTER
        )

    def select_annual_turnover(self):
        self.click(
            self.ANNUAL_TURNOVER
        )

        time.sleep(1)

        active = self.driver.switch_to.active_element

        active.send_keys(Keys.ARROW_DOWN)

        time.sleep(1)

        active.send_keys(Keys.ENTER)

        time.sleep(1)

    # =====================================================
    # ACTIONS
    # =====================================================

    def click_next(self):

        self.click(
            self.NEXT_BTN
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def is_error_visible(self):

        return any(
            e.is_displayed()
            for e in self.driver.find_elements(
                *self.ERROR_MSG
            )
        )