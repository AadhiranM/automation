from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from pages.common.base_page import BasePage
import time


class KYCPage(BasePage):

    DOB = (By.ID, "dobInput")
    FULL_NAME = (By.NAME, "full_name")
    DRIVING_LICENCE = (By.NAME, "driving_licience")
    PERSONAL_PAN = (By.ID, "kyc_pan_no")
    ADDRESS = (By.NAME, "address")
    MOBILE = (By.NAME, "mobile_no")
    ERROR_TEXT = (By.CLASS_NAME, "invalid-feedback")

    NEXT_BTN = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//button[normalize-space()='Next']"
    )

    # -------- PAGE LOAD --------
    def wait_for_page(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.DOB)
        )

    # -------- DOB --------
    def fill_dob(self, date_str):
        target_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        assert target_date < datetime.today().date()

        dob = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.DOB)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            dob, date_str
        )

    # -------- FULL NAME --------
    def fill_full_name(self, name):
        el = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(self.FULL_NAME)
        )

        self.driver.execute_script("""
            arguments[0].removeAttribute('readonly');
            arguments[0].removeAttribute('disabled');
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
            arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
        """, el, name)

        WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element(*self.PERSONAL_PAN).is_enabled()
        )

    # -------- PAN --------
    def fill_personal_pan(self, pan):
        pan_input = self.driver.find_element(*self.PERSONAL_PAN)

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
            arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
            arguments[0].dispatchEvent(new Event('blur',{bubbles:true}));
        """, pan_input, pan)

    def fill_driving_licence(self, licence):
        self.driver.find_element(*self.DRIVING_LICENCE).send_keys(licence)

    # -------- NEXT --------
    def click_next(self):
        btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.NEXT_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    # -------- VALIDATION --------
    def has_any_validation_error(self, timeout=5):
        end_time = time.time() + timeout
        while time.time() < end_time:
            if any(
                e.is_displayed() and e.text.strip()
                for e in self.driver.find_elements(*self.ERROR_TEXT)
            ):
                return True
            time.sleep(0.3)
        return False

    # =====================================================
    # 🔽 POSITIVE TEST ALIASES (NO LOGIC CHANGE)
    # =====================================================

    def select_director_dob(self, date):
        self.fill_dob(date)

    def fill_director_name(self, name):
        self.fill_full_name(name)

    def fill_director_pan(self, pan):
        self.fill_personal_pan(pan)

    def fill_director_driving_license(self, licence):
        self.fill_driving_licence(licence)

    def fill_address(self, address):
        self.driver.find_element(*self.ADDRESS).send_keys(address)

    def fill_mobile(self, mobile):
        self.driver.find_element(*self.MOBILE).send_keys(mobile)
