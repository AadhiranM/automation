import time
import os

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage
from utilities.data_generator import (
        generate_product_name,
        generate_brand_name,
        unique_id
    )


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
    #  PRODUCT IMAGE UPLOAD (FIXED)
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



    def fill_parent_form(
            self,
            manufacturer_name,
            category_name
    ):

        self.wait_for_page()

        # ---------------- PRODUCT ----------------

        self.enter_text(
            self.PRODUCT_NAME,
            generate_product_name()
        )

        # ---------------- SKU ----------------

        sku_suffix = unique_id()[-6:]

        sku_box = self.get_element(
            self.SKU_ID
        )

        sku_box.send_keys(
            sku_suffix
        )

        # ---------------- BRAND ----------------

        self.enter_text(
            self.BRAND_NAME,
            generate_brand_name()
        )

        # ---------------- MANUFACTURER ----------------

        self.select_searchable_dropdown(
            self.MANUFACTURER,
            manufacturer_name
        )

        # ---------------- CATEGORY ----------------

        self.select_searchable_dropdown(
            self.CATEGORY,
            category_name
        )

        # ---------------- STATUS ----------------

        # STATUS

        self.click(self.STATUS)

        WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(text(),'Active')]"
                )
            )
        )

        self.driver.find_element(
            By.XPATH,
            "//div[contains(text(),'Active')]"
        ).click()



        # ---------------- REGULATORY ----------------

        self.click(self.REGULATORY)

        time.sleep(1)

        self.driver.switch_to.active_element.send_keys(
            Keys.ARROW_DOWN
        )

        time.sleep(1)

        self.driver.switch_to.active_element.send_keys(
            Keys.ENTER
        )

        time.sleep(2)

        self.enter_text(
            self.REGULATORY_CODE,
            "ABCDE1234F"
        )

        # ---------------- COUNTRY ----------------

        self.click(self.COUNTRY)

        time.sleep(1)

        self.driver.switch_to.active_element.send_keys(
            Keys.ARROW_DOWN
        )

        time.sleep(1)

        self.driver.switch_to.active_element.send_keys(
            Keys.ENTER
        )

        time.sleep(2)

        # ---------------- URL ----------------

        self.enter_text(
            self.PRODUCT_URL,
            "https://test.com"
        )

        # ---------------- DESCRIPTION ----------------

        self.enter_text(
            self.DESCRIPTION,
            "Automation Product Description"
        )

        # ---------------- IMAGE ----------------

        upload_el = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.presence_of_element_located(
                self.PRODUCT_IMAGE_UPLOAD
            )
        )

        self.driver.execute_script("""
            arguments[0].style.display='block';
            arguments[0].style.visibility='visible';
            arguments[0].style.opacity='1';
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