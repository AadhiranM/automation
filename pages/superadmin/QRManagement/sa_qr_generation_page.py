from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.common.base_page import BasePage
from utilities.flatpickr import FlatpickrRangePicker
from datetime import datetime


class SAQRGenerationPage(BasePage):

    URL = "/admin/generate-qr/create"

    # =========================
    # LOCATORS (UNCHANGED)
    # =========================
    MANUFACTURER = (By.XPATH, "//label[contains(text(),'Manufacturer')]/following::div[contains(@class,'control')][1]")
    PRODUCT_ID = (By.XPATH, "//label[contains(text(),'Product ID')]/following::div[contains(@class,'control')][1]")
    VARIANT_SKU = (By.XPATH, "//label[contains(text(),'Variant SKU')]/following::div[contains(@class,'control')][1]")

    ADD_BATCH = (By.XPATH, "//input[@placeholder='Enter Batch Number']")
    QUANTITY = (By.XPATH, "//input[@placeholder='Enter Quantity']")

    PRODUCT_NAME = (By.XPATH, "//input[@placeholder='Enter Product Name']")

    MFG_DATE = (By.ID, "manufacturing_date")
    EXPIRY_DATE = (By.XPATH, "//input[@placeholder='Select Expiry Date']")

    DIMENSION = (By.XPATH, "//label[contains(text(),'Dimension')]/following::div[contains(@class,'control')][1]")
    BATCH_LOCATION = (By.XPATH, "//label[contains(text(),'Batch Location')]/following::div[contains(@class,'control')][1]")
    QR_TYPE = (By.XPATH, "//label[contains(text(),'QR Type')]/following::div[contains(@class,'control')][1]")
    QR_IMAGE_FORMAT = (By.XPATH, "//label[contains(text(),'QR Image Format')]/following::div[contains(@class,'control')][1]")

    GENERATE_BTN = (By.XPATH, "//button[contains(text(),'Generate QR')]")
    SUCCESS_MSG = (By.XPATH, "//div[contains(text(),'QR') or contains(text(),'success')]")

    # =========================
    # NAVIGATION (FIXED)
    # =========================
    def goto_page(self):
        self.driver.get(self.base_url + self.URL)

        # ✅ wait for URL change
        WebDriverWait(self.driver, 10).until(
            lambda d: "/generate-qr" in d.current_url
        )

    # =========================
    def wait_for_page(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.GENERATE_BTN)
        )

    # =========================
    # ACTION METHODS (UNCHANGED LOGIC)
    # =========================
    def select_manufacturer(self, value):
        self.select_searchable_dropdown(self.MANUFACTURER, value)

    def select_product_id(self, value):
        self.select_searchable_dropdown(self.PRODUCT_ID, value)

    def wait_for_product_autofill(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.PRODUCT_NAME).get_attribute("value") != ""
        )

    def enter_batch(self, value):
        self.enter_text(self.ADD_BATCH, value)

    def enter_quantity(self, value):
        self.enter_text(self.QUANTITY, value)

    def select_variant_sku(self, value):
        self.select_searchable_dropdown(self.VARIANT_SKU, value)

    def select_mfg_date(self, date_str):
        self.click(self.MFG_DATE)
        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(
            datetime.strptime(date_str, "%Y-%m-%d"),
            datetime.strptime(date_str, "%Y-%m-%d")
        )

    def select_expiry_date(self, date_str):
        self.click(self.EXPIRY_DATE)
        picker = FlatpickrRangePicker(self.driver)
        picker.select_range(
            datetime.strptime(date_str, "%Y-%m-%d"),
            datetime.strptime(date_str, "%Y-%m-%d")
        )

    def select_dimension(self, value):
        self.select_dropdown(self.DIMENSION, value)

    def select_batch_location(self, value):
        self.select_dropdown(self.BATCH_LOCATION, value)

    def select_qr_type(self, value):
        self.select_dropdown(self.QR_TYPE, value)

    def select_image_format(self, value):
        self.select_dropdown(self.QR_IMAGE_FORMAT, value)

    def click_generate(self):
        self.click(self.GENERATE_BTN)

    def is_qr_generated(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        )