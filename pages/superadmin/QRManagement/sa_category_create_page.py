import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage

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
        "//select[@id='manufacturer_id']/following-sibling::div"
    )

    MANUFACTURER_SEARCH = (
        By.XPATH,
        "//div[contains(@class,'choices') and contains(@class,'is-open')]//input"
    )

    MANUFACTURER_OPTION = (
        By.XPATH,
        "//div[@role='listbox']//div[contains(@class,'choices__item--choice') and contains(text(),'{name}')]"
    )

    # =========================================================
    # CATEGORY NAME
    # =========================================================
    CATEGORY_NAME = (
        By.XPATH,
        "//div[contains(@class,'modal') and contains(@class,'show')]//input[@placeholder='Enter Category Name']"
    )

    # =========================================================
    # STATUS (Choices.js)
    # =========================================================
    STATUS_DROPDOWN = (
        By.XPATH,
        "//span[@id='select2-createcategoryStatus-container']"
    )

    STATUS_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'select2-results__options')]//li[normalize-space()='{status}']"
    )

    # =========================================================
    # BUTTON
    # =========================================================
    SAVE_BTN = (By.XPATH, "//button[normalize-space()='Save']")

    # =========================================================
    # SUCCESS
    # =========================================================
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'toastify')]")

    # ============================================
    # COMMON ERROR LOCATOR
    # ============================================
    ERROR_MESSAGES = (
        By.XPATH,
        "//div[contains(@class,'invalid-feedback')]"
    )

    # ============================================
    # GET ALL ERRORS
    # ============================================
    def get_all_error_messages(self):
        elements = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.ERROR_MESSAGES)
        )
        return [el.text.strip() for el in elements if el.text.strip()]

    # ============================================
    # CHECK SPECIFIC ERROR
    # ============================================
    def is_error_present(self, text):
        errors = self.get_all_error_messages()
        return any(text.lower() in err.lower() for err in errors)

    # WAIT
    # =========================================================
    def wait_for_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MODAL)
        )

    # =========================================================
    # ACTIONS
    # =========================================================

    def select_manufacturer(self, manufacturer_email):
        self.click(self.MANUFACTURER_DROPDOWN)

        search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class,'choices') and contains(@class,'is-open')]//input[@type='search']"
            ))
        )

        search.clear()
        search.send_keys(manufacturer_email)

        time.sleep(1)

        search.send_keys(Keys.ARROW_DOWN)
        search.send_keys(Keys.ENTER)

    def enter_category_name(self, name):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CATEGORY_NAME)
        )
        self.clear(self.CATEGORY_NAME)
        self.type(self.CATEGORY_NAME, name)

    def select_status(self, status="Active"):
        # Step 1: Click dropdown
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.STATUS_DROPDOWN)
        ).click()

        # Step 2: Wait for dropdown to open
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//span[contains(@class,'select2-container--open')]"
            ))
        )

        # Step 3: Select EXACT option (STRICT locator)
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//li[@role='option' and normalize-space()='{status}']"
            ))
        )

        option.click()

        # Step 4: VERIFY selection (MANDATORY)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                self.STATUS_DROPDOWN,
                status
            )
        )

    def click_save(self):
        # Wait for button
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SAVE_BTN)
        )

        # Scroll (important sometimes)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)

        # Click using JS (bypass overlay issues)
        self.driver.execute_script("arguments[0].click();", save_btn)

    # =========================================================
    # VALIDATION
    # =========================================================
    def get_success_message(self):
        toast = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_TOAST)
        )
        return toast.text

    def wait_for_modal_to_close(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.MODAL)
        )

    def is_manufacturer_selected(self, name):
        selected = self.driver.find_element(*self.MANUFACTURER_DROPDOWN).text
        return name.lower() in selected.lower()