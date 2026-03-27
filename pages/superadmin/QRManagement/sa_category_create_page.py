from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SACategoryCreatePage(BasePage):

    # =========================================================
    # MODAL
    # =========================================================
    MODAL = (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]")

    # =========================================================
    # MANUFACTURER (Choices.js)
    # =========================================================
    MANUFACTURER_DROPDOWN = (
        By.XPATH,
        "//label[normalize-space()='Manufacturer Name']/following-sibling::div"
    )

    MANUFACTURER_SEARCH = (
        By.XPATH,
        "//div[contains(@class,'choices__list--dropdown') and contains(@class,'is-active')]//input"
    )

    MANUFACTURER_OPTIONS = (
        By.XPATH,
        "//div[contains(@class,'choices__list--dropdown') and contains(@class,'is-active')]"
        "//div[contains(@class,'choices__item--selectable')]"
    )

    # =========================================================
    # CATEGORY NAME
    # =========================================================
    CATEGORY_NAME = (
        By.XPATH,
        "//div[contains(@class,'modal') and contains(@class,'show')]//input[@placeholder='Enter Category Name']"
    )

    # =========================================================
    # STATUS (Select2)
    # =========================================================
    STATUS_DROPDOWN = (
        By.XPATH,
        "//label[normalize-space()='Status']/following-sibling::div"
    )

    # =========================================================
    # BUTTON
    # =========================================================
    SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save']")

    # =========================================================
    # SUCCESS
    # =========================================================
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'toastify')]")

    # =========================================================
    # WAIT
    # =========================================================
    def wait_for_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MODAL)
        )

    # =========================================================
    # ACTIONS
    # =========================================================

    def select_manufacturer(self, name):
        # Click dropdown
        self.click(self.MANUFACTURER_DROPDOWN)

        # Wait for dropdown active
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MANUFACTURER_SEARCH)
        )

        # Type search
        search = self.driver.find_element(*self.MANUFACTURER_SEARCH)
        search.clear()
        search.send_keys(name)

        # Wait for options
        options = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.MANUFACTURER_OPTIONS)
        )

        # Click matching option
        for opt in options:
            if name.lower() in opt.text.lower():
                self.driver.execute_script("arguments[0].click();", opt)
                return

        raise Exception(f"Manufacturer '{name}' not found")

    def enter_category_name(self, name):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CATEGORY_NAME)
        )
        self.clear(self.CATEGORY_NAME)
        self.type(self.CATEGORY_NAME, name)

    def select_status(self, status="Active"):
        # Click dropdown
        self.click(self.STATUS_DROPDOWN)

        # Wait for dropdown open
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[contains(@class,'select2-container--open')]"
            ))
        )

        # Select option
        option = (
            By.XPATH,
            f"//li[contains(@class,'select2-results__option') and normalize-space()='{status}']"
        )

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(option)
        ).click()

    def click_save(self):
        self.click(self.SAVE_BTN)

    # =========================================================
    # VALIDATION
    # =========================================================
    def get_success_message(self):
        toast = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_TOAST)
        )
        return toast.text