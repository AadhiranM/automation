import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
class SAQRGenerationPage(BasePage):

    URL = "/admin/generate-qr/create"

    # =========================
    # DROPDOWNS (SEARCH TYPE)
    # =========================
    MANUFACTURER = (By.XPATH, "//label[contains(text(),'Manufacturer')]/following::div[contains(@class,'choices__inner')][1]")
    PRODUCT_ID = (By.XPATH, "//label[contains(text(),'Product ID')]/following::div[contains(@class,'choices__inner')][1]")
    VARIANT_SKU = (By.XPATH, "//label[contains(text(),'Variant SKU')]/following::div[contains(@class,'choices__inner')][1]")
    BATCH_LOCATION = (By.XPATH, "//label[contains(text(),'Batch Location')]/following::div[contains(@class,'choices__inner')][1]")

    # =========================
    # INPUT FIELDS
    # =========================
    BATCH = (By.XPATH, "//input[@placeholder='Enter Batch Number']")
    QUANTITY = (By.XPATH, "//input[@placeholder='Enter Quantity']")

    # =========================
    # DATE INPUT
    # =========================
    MFG_DATE = (By.ID, "manufacturing_date")
    EXPIRY_DATE = (By.XPATH, "//input[@placeholder='Select Expiry Date']")

    # =========================
    # DROPDOWNS (CHOICES.JS)
    # =========================
    DIMENSION = (By.XPATH, "//label[contains(text(),'Dimension')]/following::div[contains(@class,'choices__inner')][1]")
    QR_TYPE = (By.XPATH, "//label[contains(text(),'QR Type')]/following::div[contains(@class,'choices__inner')][1]")
    IMAGE_FORMAT = (By.XPATH, "//label[contains(text(),'QR Image Format')]/following::div[contains(@class,'choices__inner')][1]")

    # =========================
    # BUTTON
    # =========================
    GENERATE_BTN = (By.XPATH, "//button[.//span[contains(text(),'Generate QR')]]")

    # =========================
    # NAVIGATION
    # =========================
    def goto_page(self):
        self.driver.get("https://beta.digitathya.com/admin/generate-qr/create")

    def wait_for_page(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.MANUFACTURER)
        )

    # =========================
    # 🔥 COMMON DROPDOWN CLOSE
    # =========================
    def close_dropdown(self):
        try:
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)
        except:
            pass

    # =========================
    # SEARCH DROPDOWNS
    # =========================
    def select_manufacturer_dynamic(
            self,
            manufacturer_name
    ):

        self.select_searchable_dropdown(
            self.MANUFACTURER,
            manufacturer_name
        )

        self.close_dropdown()

    def select_product_id_dynamic(self, sku_id):

        for attempt in range(2):

            self.select_searchable_dropdown(
                self.PRODUCT_ID,
                sku_id
            )

            try:

                WebDriverWait(self.driver, 20).until(
                    lambda d:
                    d.find_element(
                        By.XPATH,
                        "//input[@placeholder='Enter Product Name']"
                    ).get_attribute("value").strip() != ""
                )

                return

            except:

                print(
                    f"Product load failed. Retry {attempt + 1}"
                )

        raise Exception(
            "Product details not loaded"
        )

    def select_variant_sku(self):

        self.click(self.VARIANT_SKU)

        time.sleep(2)

        options = self.driver.find_elements(
            By.XPATH,
            "//div[@data-choice-selectable]"
        )

        valid_options = [
            opt for opt in options
            if opt.text.strip()
        ]

        if not valid_options:
            print("No Variant SKU available. Continuing without variant.")
            return False

        print(
            f"Selected Variant SKU: {valid_options[0].text}"
        )

        self.driver.execute_script(
            "arguments[0].click();",
            valid_options[0]
        )

        time.sleep(1)

        return True

    # INPUT METHODS
    # =========================
    def enter_batch(self, value):
        self.enter_text(self.BATCH, value)

    def enter_quantity(self, value):
        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.element_to_be_clickable(self.QUANTITY))

        # 🔥 force focus
        self.driver.execute_script("arguments[0].focus();", el)

        # 🔥 HARD CLEAR
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)

        # 🔥 JS SET VALUE (THIS IS THE REAL FIX)
        self.driver.execute_script("arguments[0].value = arguments[1];", el, value)

        # 🔥 TRIGGER INPUT EVENT (CRITICAL)
        self.driver.execute_script("""
            arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
        """, el)

        # 🔥 blur to register validation
        el.send_keys(Keys.TAB)

        time.sleep(1)

    # =========================
    # DATE METHODS
    # =========================
    def select_mfg_date(self, value):
        el = self.get_element(self.MFG_DATE)
        self.driver.execute_script("arguments[0].value = arguments[1]", el, value)

    def select_expiry_date(self, value):
        el = self.get_element(self.EXPIRY_DATE)
        self.driver.execute_script("arguments[0].value = arguments[1]", el, value)


    # =========================
    # CHOICES.JS DROPDOWNS
    # =========================
    def select_dimension(self, value):
        self.select_status_keyboard(self.DIMENSION, value)
        self.close_dropdown()


    def select_image_format(self, value):
        self.select_status_keyboard(self.IMAGE_FORMAT, value)
        self.close_dropdown()

    # =========================
    # ACTION
    # =========================
    def click_generate(self):
        wait = WebDriverWait(self.driver, 15)

        btn = wait.until(EC.presence_of_element_located(self.GENERATE_BTN))

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(1)

        wait.until(EC.element_to_be_clickable(self.GENERATE_BTN))

        try:
            btn.click()
        except:
            print("⚠️ Normal click failed → using JS click")
            self.driver.execute_script("arguments[0].click();", btn)

    def close_calendar_overlay(self):

        try:

            calendar = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"
            )

            self.driver.execute_script(
                "arguments[0].style.display='none';",
                calendar
            )

        except:
            pass

    # def select_batch_location(self, value="Chennai"):
    #
    #     self.select_searchable_dropdown(
    #         self.BATCH_LOCATION,
    #         value
    #     )
    #
    #     self.close_dropdown()
    #
    #     time.sleep(1)

    def select_batch_location(self, value="Chennai"):

        self.select_searchable_dropdown(
            self.BATCH_LOCATION,
            value
        )

        ActionChains(self.driver) \
            .send_keys(Keys.TAB) \
            .perform()

        time.sleep(1)

    def select_qr_type(self):

        self.click(self.QR_TYPE)

        time.sleep(1)

        ActionChains(self.driver) \
            .send_keys(Keys.ARROW_DOWN) \
            .send_keys(Keys.ENTER) \
            .perform()

        time.sleep(1)