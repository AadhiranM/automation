import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage

# ✅ GLOBAL FILE PATH (PIPELINE SAFE)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
FILE_PATH = os.path.join(BASE_DIR, "test_data", "images", "selenium_image.jpg")


class SAProductCreateParentPage(BasePage):

    # =========================
    # TEXT FIELDS
    # =========================
    PRODUCT_NAME = (By.ID, "product_name")
    SKU_ID = (By.XPATH, "//input[@placeholder='Enter SKU ID']")
    BRAND_NAME = (By.XPATH, "//input[@placeholder='Enter Brand Name']")
    DESCRIPTION = (By.XPATH, "//textarea[@placeholder='Enter Product Description']")
    PRODUCT_URL = (By.XPATH, "//input[@placeholder='Enter Product URL']")
    REGULATORY_CODE = (By.ID, "regulatory_codes")

    # =========================
    # DROPDOWNS
    # =========================
    MANUFACTURER = (By.XPATH, "//select[@id='manufacturer_id']/following-sibling::div")
    CATEGORY = (By.XPATH, "//select[@id='category_id']/following-sibling::div")
    STATUS = (By.XPATH, "//select[@id='product_status']/following-sibling::div")
    REGULATORY = (By.XPATH, "//select[@id='regulatory_id']/following-sibling::div")
    COUNTRY = (By.XPATH, "//select[@id='country_id']/following-sibling::div")

    # =========================
    # ✅ PRODUCT IMAGE UPLOAD (FIXED)
    # =========================
    PRODUCT_IMAGE_UPLOAD = (By.ID, "imageUpload")

    # =========================
    # BUTTON
    # =========================
    PROCEED_BTN = (By.XPATH, "//button[contains(text(),'Proceed to Child SKU')]")

    def wait_for_page(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.PRODUCT_NAME)
        )

    def fill_parent_form(self):
        self.wait_for_page()

        # ---------- TEXT ----------
        self.enter_text(self.PRODUCT_NAME, "Test Product Auto")
        self.enter_text(self.SKU_ID, "AUTO12345")
        self.enter_text(self.BRAND_NAME, "Test Brand")

        # ---------- DROPDOWNS ----------
        self.select_searchable_dropdown(self.MANUFACTURER, "Sydneyyy Tea Shop")
        self.select_searchable_dropdown(self.CATEGORY, "BerlinAutomateTest")

        # ---------- STATUS ----------
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.STATUS)
        )
        self.select_status_keyboard(self.STATUS, "Active")

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((
                By.XPATH, "//div[contains(@class,'choices__list--dropdown')]"
            ))
        )

        # ---------- REGULATORY ----------
        self.select_searchable_dropdown(self.REGULATORY, "PAN")

        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.REGULATORY_CODE).get_attribute("readonly") is None
        )

        self.enter_text(self.REGULATORY_CODE, "ABCDE1234F")

        # ---------- COUNTRY ----------
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.COUNTRY)
        )
        self.select_searchable_dropdown(self.COUNTRY, "India")

        time.sleep(1)

        # ---------- SCROLL ----------
        desc = self.get_element(self.DESCRIPTION)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", desc)

        # ---------- OTHER ----------
        self.enter_text(self.PRODUCT_URL, "https://test.com")
        self.enter_text(self.DESCRIPTION, "Automation Description")

        # =========================
        # ✅ PRODUCT IMAGE UPLOAD (FINAL FIX)
        # =========================
        upload_el = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PRODUCT_IMAGE_UPLOAD)
        )

        # 🔥 make visible (if hidden)
        self.driver.execute_script("""
            arguments[0].style.display = 'block';
            arguments[0].style.visibility = 'visible';
            arguments[0].style.opacity = 1;
        """, upload_el)

        upload_el.send_keys(FILE_PATH)

        time.sleep(2)

        # ---------- PROCEED ----------
        self.go_to_child()


    def go_to_child(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PROCEED_BTN)
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)

        try:
            btn.click()
        except:
            print("Normal click failed → using JS click")
            self.driver.execute_script("arguments[0].click();", btn)