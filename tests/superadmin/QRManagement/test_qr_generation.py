import pytest
import time
import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.QRManagement.sa_qr_generation_page import (
    SAQRGenerationPage
)
from pages.superadmin.QRManagement.sa_qr_list_page import (
    SAQRListPage
)
from pages.superadmin.QRManagement.sa_product_list_page import (
    SAProductListPage
)
from datetime import date, timedelta

@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestQRGeneration:

    def generate_batch(self):

        return (
            "BI"
            + ''.join(
                random.choices(
                    string.digits,
                    k=5
                )
            )
            + "-"
            + ''.join(
                random.choices(
                    string.ascii_lowercase,
                    k=6
                )
            )
        )

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_generate_qr_success(
            self,
            login_superadmin
    ):

        driver = login_superadmin["driver"]

        # =====================================================
        # STEP 1 - GET PRODUCT DATA
        # =====================================================

        product_page = SAProductListPage(driver)

        product_page.goto_page()

        product_page.wait_for_page()

        manufacturer_name, product_name, sku_id = (
            product_page.get_first_product_data()
        )

        print("Manufacturer :", manufacturer_name)
        print("Product Name :", product_name)
        print("SKU ID :", sku_id)

        # =====================================================
        # STEP 2 - OPEN QR PAGE
        # =====================================================

        qr = SAQRGenerationPage(driver)

        qr.goto_page()

        qr.wait_for_page()

        # =====================================================
        # STEP 3 - MANUFACTURER
        # =====================================================

        qr.select_manufacturer_dynamic(
            manufacturer_name
        )

        time.sleep(2)

        # =====================================================
        # STEP 4 - PRODUCT ID
        # =====================================================

        qr.select_product_id_dynamic(
            sku_id
        )

        time.sleep(3)

        # =====================================================
        # STEP 5 - BATCH
        # =====================================================

        batch_no = self.generate_batch()

        print("Generated Batch :", batch_no)

        qr.enter_batch(batch_no)

        # =====================================================
        # STEP 6 - VARIANT SKU
        # =====================================================

        qr.select_variant_sku()

        time.sleep(1)

        # =====================================================
        # STEP 7 - QUANTITY
        # =====================================================

        qr.enter_quantity("10")

        # =====================================================
        # STEP 8 - DATES
        # =====================================================

        mfg_date = (
                date.today() + timedelta(days=10)
        ).strftime("%Y-%m-%d")

        expiry_date = (
                date.today() + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        print("Manufacturing Date :", mfg_date)
        print("Expiry Date :", expiry_date)

        qr.select_mfg_date(mfg_date)

        time.sleep(1)

        qr.select_expiry_date(expiry_date)

        qr.close_calendar_overlay()

        time.sleep(1)
        # =====================================================
        # STEP 9 - BATCH LOCATION
        # =====================================================

        batch_location = "Chennai"

        qr.select_batch_location(batch_location)

        time.sleep(1)

        # =====================================================
        # STEP 10 - DIMENSION
        # =====================================================

        qr.select_dimension()

        time.sleep(1)


        # =====================================================
        # STEP 12 - IMAGE FORMAT
        # =====================================================

        qr.select_image_format()

        time.sleep(1)

        # =====================================================
        # STEP 13 - GENERATE QR
        # =====================================================

        qr.click_generate()

        # =====================================================
        # SUCCESS TOAST
        # =====================================================

        WebDriverWait(
            driver,
            15
        ).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'toast')]"
                )
            )
        )

        time.sleep(5)

        # =====================================================
        # STEP 14 - VALIDATION
        # =====================================================

        # =====================================================
        # STEP 14 - VALIDATION
        # =====================================================

        qr_list = SAQRListPage(driver)

        qr_list.goto_page()

        time.sleep(3)

        latest_batch = qr_list.get_first_batch_text()

        print("Latest Batch :", latest_batch)

        # Get only unique random suffix
        random_part = batch_no.split("-")[1]

        print("Random Part :", random_part)

        assert random_part in latest_batch, (
            f"Generated batch not found. "
            f"Expected random part={random_part}, "
            f"Actual={latest_batch}"
        )

        print("QR Batch Validation Passed")