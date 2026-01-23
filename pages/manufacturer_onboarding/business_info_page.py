from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.common.base_page import BasePage
import time


class BusinessInfoPage(BasePage):

    COMPANY_NAME = (By.ID, "companyNameInput")
    BUSINESS_EMAIL = (By.NAME, "business_email")
    NEXT_BTN = (By.XPATH, "//button[normalize-space()='Next']")
    ERROR_MSG = (By.XPATH, "//div[contains(@class,'invalid-feedback')]")

    # 🔽 ADDITIONS (for POSITIVE only)
    GST = (By.NAME, "gst_no")
    PAN = (By.NAME, "pan_no")
    WEBSITE = (By.NAME, "website_url")
    ANNUAL_TURNOVER = (By.ID, "annual_turnover")

    BUSINESS_TYPE = (By.XPATH, "//span[contains(@id,'select2-business_type_id-container')]")
    INDUSTRY = (By.XPATH, "//span[contains(@id,'select2-industry_type_id-container')]")
    SELECT2_INPUT = (By.CLASS_NAME, "select2-search__field")

    DATE_OF_INCORP = (
        By.XPATH,
        "//input[contains(@class,'flatpickr-input') and @placeholder='DD-MM-YYYY']"
    )

    # -------- PAGE LOAD --------
    def wait_for_page(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.COMPANY_NAME)
        )

    # -------- ACTIONS --------
    def fill_company_name(self, name):
        self.type(self.COMPANY_NAME, name)

    def fill_business_email(self, email):
        self.type(self.BUSINESS_EMAIL, email)

    def click_next(self):
        self.click(self.NEXT_BTN)

    def goto_page(self):
        self.driver.get(
            "https://beta.digitathya.com/admin/manufacturer/onboarding"
        )

    # -------- VALIDATION --------
    def has_any_validation_error(self, timeout=5):
        end_time = time.time() + timeout
        while time.time() < end_time:

            if any(
                e.is_displayed() and e.text.strip()
                for e in self.driver.find_elements(*self.ERROR_MSG)
            ):
                return True

            toast = self.driver.execute_script("""
                let t = document.querySelector('.toast.show .toast-body');
                return t ? t.innerText : null;
            """)
            if toast:
                print("🔴 BUSINESS INFO TOAST:", toast)
                return True

            time.sleep(0.3)
        return False

    def is_error_visible(self):
        return any(
            e.is_displayed() for e in self.driver.find_elements(*self.ERROR_MSG)
        )

    def get_company_name_error(self):
        return self.driver.find_element(
            By.XPATH,
            "//input[@id='companyNameInput']/following-sibling::div[@class='invalid-feedback']"
        ).text.strip()

    def get_toast_message(self, timeout=10):
        toast = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast-body"))
        )
        return toast.text.strip()

    # =====================================================
    # 🔽 POSITIVE FLOW SUPPORT (ADDED, SAFE)
    # =====================================================

    def fill_date_of_incorporation(self, date_str):
        el = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.DATE_OF_INCORP)
        )
        self.driver.execute_script(
            "arguments[0]._flatpickr.setDate(arguments[1], true);",
            el, date_str
        )

    def select_business_type(self, value):
        self.click(self.BUSINESS_TYPE)
        self.type(self.SELECT2_INPUT, value)
        self.type(self.SELECT2_INPUT, Keys.ENTER)

    def select_industry(self, value):
        self.click(self.INDUSTRY)
        self.type(self.SELECT2_INPUT, value)
        self.type(self.SELECT2_INPUT, Keys.ENTER)

    def fill_gst(self, gst):
        self.type(self.GST, gst)

    def fill_pan(self, pan):
        self.type(self.PAN, pan)

    def fill_website(self, url):
        self.type(self.WEBSITE, url)

    def select_annual_turnover(self, value):
        self.select_by_visible_text(self.ANNUAL_TURNOVER, value)
