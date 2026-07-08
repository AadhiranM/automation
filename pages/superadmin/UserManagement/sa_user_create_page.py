from pages.common.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class SAUserCreatePage(BasePage):

    # =====================================================
    # INPUTS
    # =====================================================

    NAME_INPUT = (
        By.XPATH,
        "//input[@placeholder='Enter User Name']"
    )

    EMAIL_INPUT = (
        By.XPATH,
        "//input[@placeholder='Enter Email ID']"
    )

    MOBILE_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'10-digit')]"
    )

    PASSWORD_INPUT = (
        By.XPATH,
        "//input[@type='password']"
    )

    # =====================================================
    # DROPDOWNS
    # =====================================================

    ROLE_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Role')]/following::div[contains(@class,'choices')][1]"
    )

    STATUS_DROPDOWN = (
        By.XPATH,
        "//label[contains(text(),'Status')]/following::div[contains(@class,'choices')][1]"
    )

    # =====================================================
    # BUTTONS
    # =====================================================

    SUBMIT_BTN = (
        By.XPATH,
        "//button[contains(text(),'Submit')]"
    )

    SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(text(),'successfully')]"
    )

    # =====================================================
    # PAGE
    # =====================================================

    MANUFACTURER_CHECKBOX = (
        By.XPATH,
        "//input[@type='checkbox' and @name='create_under_manufacturer']"
    )

    MANUFACTURER_DROPDOWN = (
        By.XPATH,
        "//select[@id='selected_manufacturer_id']/following-sibling::div[contains(@class,'choices')]"
    )

    MANUFACTURER_SEARCH = (
        By.XPATH,
        "//span[contains(@class,'select2-container')]//input[@type='search']"
    )

    FIRST_MANUFACTURER = (
        By.XPATH,
        "(//div[@class='choices__list' and @role='listbox']//div[@role='option'])[1]"
    )

    def goto_page(self):

        self.driver.get(
            "https://beta.digitathya.com/admin/user/create"
        )

    # =====================================================
    # INPUT METHODS
    # =====================================================

    def enter_name(self, name):
        self.type(self.NAME_INPUT, name)

    def enter_email(self, email):
        self.type(self.EMAIL_INPUT, email)

    def enter_mobile(self, mobile):
        self.type(self.MOBILE_INPUT, mobile)

    def enter_password(self, password):
        self.type(self.PASSWORD_INPUT, password)

    # =====================================================
    # ROLE DROPDOWN
    # =====================================================

    def select_role(self):

        wait = WebDriverWait(self.driver, 30)

        dropdown = wait.until(
            EC.element_to_be_clickable(
                self.ROLE_DROPDOWN
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        ActionChains(self.driver)\
            .move_to_element(dropdown)\
            .click()\
            .perform()

        print("Role dropdown opened")

        time.sleep(2)

        active = self.driver.switch_to.active_element

        # active.send_keys(Keys.ARROW_DOWN)
        #
        # time.sleep(1)
        #
        # active.send_keys(Keys.ENTER)
        active.send_keys(Keys.ENTER)
        time.sleep(2)

        print("Role selected")

    # =====================================================
    # STATUS DROPDOWN
    # =====================================================

    def select_status(self, status):
        wait = WebDriverWait(self.driver, 30)

        # open dropdown
        dropdown = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//span[@id='select2-idSelectcustom-container']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        ActionChains(self.driver) \
            .move_to_element(dropdown) \
            .click() \
            .perform()

        print("Status dropdown opened")

        time.sleep(2)

        # select option
        option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[contains(@class,'select2-results__option') and normalize-space()='{status}']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            option
        )

        time.sleep(1)

        ActionChains(self.driver) \
            .move_to_element(option) \
            .click() \
            .perform()

        print(f"{status} selected")

        time.sleep(2)


    # =====================================================
    # SUBMIT
    # =====================================================

    def click_submit(self):

        self.safe_click(self.SUBMIT_BTN)

    # =====================================================
    # COMPLETE FLOW
    # =====================================================

    def create_user(
            self,
            name,
            email,
            manufacturer,
            mobile,
            password,
            status="Active"
    ):

        self.enter_name(name)

        self.enter_email(email)

        self.select_manufacturer(manufacturer)

        self.select_role()

        self.select_status(status)

        self.enter_mobile(mobile)

        self.enter_password(password)

        self.click_submit()

    def select_manufacturer(self, manufacturer):
        wait = WebDriverWait(self.driver, 20)

        # Enable Manufacturer
        self.safe_click(self.MANUFACTURER_CHECKBOX)
        time.sleep(1)

        # Open dropdown
        self.safe_click(self.MANUFACTURER_DROPDOWN)
        time.sleep(1)

        # Click search box
        search = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@type='search' and contains(@class,'choices__input')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            search
        )

        time.sleep(1)

        # Type into the active element
        active = self.driver.switch_to.active_element
        active.send_keys(manufacturer)

        print("Typed manufacturer :", manufacturer)

        time.sleep(2)

        active.send_keys(Keys.ENTER)

        time.sleep(2)