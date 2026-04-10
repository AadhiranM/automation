from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage


class SAVariantCreatePage(BasePage):

    PAGE_LOADED = (By.XPATH, "//button[contains(text(),'Save Variants')]")

    # ==========================
    # SELECT2 DROPDOWNS
    # ==========================
    MANUFACTURER_DROPDOWN = (By.XPATH, "//select[@id='manufacturer_id']/following-sibling::span")
    CATEGORY_DROPDOWN = (By.XPATH, "//select[@id='category_id']/following-sibling::span")

    SELECT2_SEARCH_INPUT = (By.XPATH, "//span[contains(@class,'select2-container--open')]//input")

    # ==========================
    # VARIANT INPUTS
    # ==========================
    VARIANT_TYPE = (By.XPATH, "//input[@placeholder='Enter Variant Type']")
    VARIANT_VALUE = (By.XPATH, "//input[@placeholder='Enter Variant Value']")
    UPDATE_BTN = (By.XPATH, "//button[contains(@class,'variant-submit-btn')]")
    # ==========================
    # BUTTONS
    # ==========================
    ADD_MORE_VARIANTS_BTN = (By.XPATH, "//button[contains(@class,'add-variant-btn')]")
    ADD_VARIANT_VALUE_BTN = (By.XPATH, "//button[contains(@class,'add-row-btn')]")
    DELETE_VARIANT_VALUE_BTN = (By.XPATH, "//button[contains(@class,'cmn_remove')]")
    REMOVE_VARIANT_SECTION_BTN = (By.XPATH, "//button[contains(@class,'remove-card-btn')]")
    SAVE_BTN = (By.XPATH, "//button[contains(text(),'Save Variants')]")

    # ==========================
    # TOAST
    # ==========================
    TOAST_MESSAGE = (By.XPATH, "//div[contains(@class,'toastify')]")

    ERROR_MESSAGES = (By.XPATH, "//div[contains(@class,'invalid-feedback')]")

    # ==========================
    # WAIT
    # ==========================
    def wait_for_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PAGE_LOADED)
        )

    # ==========================
    # SELECT2 HANDLING
    # ==========================
    def select_from_select2(self, dropdown_locator, value):
        self.click(dropdown_locator)

        search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SELECT2_SEARCH_INPUT)
        )

        search.clear()
        search.send_keys(value)

        # ✅ WAIT UNTIL THE EXPECTED TEXT APPEARS IN DROPDOWN
        option = WebDriverWait(self.driver, 15).until(
            lambda d: next(
                (
                    el for el in d.find_elements(
                    By.XPATH,
                    "//li[contains(@class,'select2-results__option')]"
                )
                    if value.lower() in el.text.lower()
                ),
                None
            )
        )

        if not option:
            raise Exception(f"Value '{value}' not found in dropdown")

        # ✅ SCROLL + CLICK
        self.driver.execute_script("arguments[0].scrollIntoView(true);", option)

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(option)
        )

        option.click()

        # ✅ WAIT UNTIL DROPDOWN CLOSES
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.SELECT2_SEARCH_INPUT)
        )

    def select_manufacturer(self, name):
        self.select_from_select2(self.MANUFACTURER_DROPDOWN, name)

    def select_category(self, name):
        self.select_from_select2(self.CATEGORY_DROPDOWN, name)

    # ==========================
    # INPUT HANDLING
    # ==========================
    def enter_variant_type(self, text, index=0):
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.VARIANT_TYPE)) > index
        )

        elements = self.driver.find_elements(*self.VARIANT_TYPE)
        elements[index].clear()
        elements[index].send_keys(text)

    def enter_variant_value(self, text, index=0):
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.VARIANT_VALUE)) > index
        )

        elements = self.driver.find_elements(*self.VARIANT_VALUE)
        elements[index].clear()
        elements[index].send_keys(text)

    # ==========================
    # ACTIONS (STABLE)
    # ==========================
    def click_add_more_variants(self):
        old_count = len(self.driver.find_elements(*self.VARIANT_TYPE))

        self.click(self.ADD_MORE_VARIANTS_BTN)

        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.VARIANT_TYPE)) > old_count
        )

    def click_add_variant_value(self):
        old_count = len(self.driver.find_elements(*self.VARIANT_VALUE))

        self.click(self.ADD_VARIANT_VALUE_BTN)

        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(*self.VARIANT_VALUE)) > old_count
        )

    def click_delete_variant_value(self, index=0):
        buttons = self.driver.find_elements(*self.DELETE_VARIANT_VALUE_BTN)

        if len(buttons) > index:
            old_count = len(self.driver.find_elements(*self.VARIANT_VALUE))

            buttons[index].click()

            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(*self.VARIANT_VALUE)) < old_count
            )
        else:
            print("⚠️ No variant value to delete")

    def click_remove_variant_section(self, index=0):
        buttons = self.driver.find_elements(*self.REMOVE_VARIANT_SECTION_BTN)

        if len(buttons) > index:
            old_count = len(self.driver.find_elements(*self.VARIANT_TYPE))

            buttons[index].click()

            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(*self.VARIANT_TYPE)) < old_count
            )
        else:
            print("⚠️ No variant section available to remove")

    def click_save(self):
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SAVE_BTN)
        )

        # 🔥 Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)

        # 🔥 Wait until clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SAVE_BTN)
        )

        try:
            save_btn.click()
        except:
            # fallback (very important for UI overlap issues)
            self.driver.execute_script("arguments[0].click();", save_btn)

    # ==========================
    # ERRORS
    # ==========================
    def get_all_errors(self):
        elements = self.driver.find_elements(*self.ERROR_MESSAGES)
        return [e.text for e in elements if e.text.strip()]

    def is_error_present(self, text):
        return any(text.lower() in e.lower() for e in self.get_all_errors())

    # ==========================
    # TOAST HANDLING (BEST)
    # ==========================
    def get_toast_message(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.TOAST_MESSAGE)
            )
            print("Toast:", element.text)  # debug
            return element.text.strip()
        except:
            return ""

    def is_variant_saved_successfully(self):
        return "success" in self.get_toast_message().lower()

    def is_save_button_disabled(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SAVE_BTN)
        )
        return not btn.is_enabled()

    def is_save_button_enabled(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SAVE_BTN)
        )
        return btn.is_enabled()

    def is_toast_message_displayed(self, text):
        try:
            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//*[contains(text(),'{text}')]")
                )
            )
            return toast.is_displayed()
        except:
            return False

    def click_category_dropdown(self):
        self.click(self.CATEGORY_DROPDOWN)

    def is_transient_error_present(self, text):
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: any(
                    text.lower() in el.text.lower()
                    for el in d.find_elements(By.XPATH, "//span[contains(@class,'invalid-feedback')]")
                )
            )
            return True
        except:
            return False

    def click_update(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'variant-submit-btn')]"))
        )

        # ✅ scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)

        # small wait (UI animation fix)
        import time
        time.sleep(1)

        # ✅ JS click (strong fix)
        self.driver.execute_script("arguments[0].click();", btn)