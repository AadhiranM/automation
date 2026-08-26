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
    __test__ = False

    def generate_batch(self):
        return (
                "B19533-I"
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

    def create_fresh_completed_batch(self, driver):
        """
        Generate a completely fresh QR batch and move it to Completed.

        Returns:
            batch_no
        """

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
        # STEP 2 - OPEN QR GENERATION
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
        # STEP 4 - PRODUCT
        # =====================================================

        qr.select_product_id_dynamic(
            sku_id
        )

        time.sleep(3)

        # =====================================================
        # STEP 5 - FRESH BATCH
        # =====================================================

        batch_no = self.generate_batch()

        print(
            "Fresh Batch Created :",
            batch_no
        )
        print("=" * 60)
        print(f"CREATED BATCH VALUE : [{batch_no}]")
        print(f"CURRENT URL         : {driver.current_url}")
        print("=" * 60)

        qr.enter_batch(batch_no)

        # =====================================================
        # STEP 6 - VARIANT
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

        qr.select_mfg_date(mfg_date)

        time.sleep(1)

        qr.select_expiry_date(expiry_date)

        qr.close_calendar_overlay()

        time.sleep(1)

        # =====================================================
        # STEP 9 - LOCATION
        # =====================================================

        qr.select_batch_location("Chennai")

        time.sleep(1)

        # =====================================================
        # STEP 10 - DIMENSION
        # =====================================================

        qr.select_dimension()

        time.sleep(1)

        # =====================================================
        # STEP 11 - IMAGE FORMAT
        # =====================================================

        qr.select_image_format()

        time.sleep(1)

        # =====================================================
        # STEP 12 - GENERATE
        # =====================================================

        qr.click_generate()

        # =====================================================
        # STEP 13 - SUCCESS TOAST
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
        # STEP 14 - OPEN QR LIST
        # =====================================================

        qr_list = SAQRListPage(driver)

        qr_list.goto_page()

        qr_list.wait_for_page()

        # =====================================================
        # GET ACTUAL BATCH NUMBER FROM QR MANAGEMENT LIST
        # =====================================================

        actual_batch = WebDriverWait(
            driver,
            30,
            poll_frequency=0.5
        ).until(
            lambda d: (
                    d.find_element(
                        By.XPATH,
                        "(//table//tbody//tr[1]//td)[4]"
                    ).text.strip()
                    or False
            )
        )

        print("=" * 60)
        print(f"GENERATED BATCH : [{batch_no}]")
        print(f"ACTUAL LIST BATCH : [{actual_batch}]")
        print("=" * 60)

        # =====================================================
        # SEARCH ACTUAL BATCH NUMBER
        # =====================================================

        qr_list.search_batch(actual_batch)

        qr_list.wait_for_batch(actual_batch)

        batch_no = actual_batch

        print(
            "Fresh batch found:",
            batch_no
        )

        # =====================================================
        # STEP 16 - QR GENERATED
        # =====================================================

        qr_list.verify_batch_status(
            batch_no,
            "QR Generated"
        )

        # =====================================================
        # STEP 17 - IN PRINT
        # =====================================================

        qr_list.update_batch_status(
            batch_no,
            "In Print",
            "Moving QR batch to In Print"
        )

        qr_list.wait_for_batch_status(
            batch_no,
            "In Print"
        )

        qr_list.verify_batch_status(
            batch_no,
            "In Print"
        )

        # =====================================================
        # STEP 18 - IN TRANSIT
        # =====================================================

        qr_list.update_batch_status(
            batch_no,
            "In Transit",
            "Moving QR batch to In Transit"
        )

        qr_list.wait_for_batch_status(
            batch_no,
            "In Transit"
        )

        qr_list.verify_batch_status(
            batch_no,
            "In Transit"
        )

        # =====================================================
        # STEP 19 - COMPLETED
        # =====================================================

        qr_list.update_batch_status(
            batch_no,
            "Completed",
            "Completing QR batch"
        )

        qr_list.wait_for_batch_status(
            batch_no,
            "Completed"
        )

        qr_list.verify_batch_status(
            batch_no,
            "Completed"
        )

        print(
            "Fresh batch completed:",
            batch_no
        )

        return batch_no

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


    # =====================================================
    # QR LIFECYCLE TEST
    # =====================================================

    # =====================================================
    # QR LIFECYCLE
    # =====================================================

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_qr_lifecycle(self, login_superadmin):
        driver = login_superadmin["driver"]

        # =====================================================
        # STEP 1 - OPEN QR MANAGEMENT
        # =====================================================

        qr_list = SAQRListPage(driver)

        qr_list.goto_page()

        qr_list.wait_for_page()

        # =====================================================
        # STEP 2 - SEARCH LATEST BATCH
        # =====================================================

        batch_no = qr_list.get_first_batch_text()

        print(
            "Lifecycle Batch :",
            batch_no
        )

        assert batch_no, (
            "No QR batch found"
        )

        qr_list.search_batch(batch_no)

        # =====================================================
        # STEP 3 - VERIFY QR GENERATED
        # =====================================================

        qr_list.wait_for_batch(
            batch_no
        )

        qr_list.verify_batch_status(
            batch_no,
            "QR Generated"
        )


        # STEP 5 - MOVE TO IN PRINT
        # =====================================================

        qr_list.update_batch_status(
            batch_no,
            "In Print",
            "Moving QR batch to In Print"
        )

        qr_list.wait_for_batch_status(
            batch_no,
            "In Print"
        )

        qr_list.verify_batch_status(
            batch_no,
            "In Print"
        )



        # =====================================================
        # STEP 6 - MOVE TO IN TRANSIT
        # =====================================================

        qr_list.update_batch_status(
            batch_no,
            "In Transit",
            "Moving QR batch to In Transit"
        )

        qr_list.wait_for_batch_status(
            batch_no,
            "In Transit"
        )

        qr_list.verify_batch_status(
            batch_no,
            "In Transit"
        )

        # =====================================================
        # STEP 7 - MOVE TO COMPLETED
        # =====================================================

        qr_list.update_batch_status(
            batch_no,
            "Completed",
            "Completing QR batch"
        )

        qr_list.wait_for_batch_status(
            batch_no,
            "Completed"
        )

        # qr_list.verify_batch_status(
        #     batch_no,
        #     "Completed"
        # )
        #
        # qr_list.verify_tracking_status(
        #     batch_no,
        #     "Completed"
        # )

        # =====================================================
        # STEP 8 - DOWNLOAD COMPLETED BATCH
        # =====================================================

        batch_zip, pdf_zip = qr_list.download_batch(
            batch_no
        )

        print("Batch ZIP :", batch_zip)
        print("PDF ZIP   :", pdf_zip)

        assert batch_zip, (
            "Completed QR Batch ZIP download failed"
        )

        assert pdf_zip, (
            "Completed QR PDF ZIP download failed"
        )

        print(
            "Batch ZIP download validation passed"
        )

        print(
            "PDF ZIP download validation passed"
        )

        print(
            "QR Lifecycle Completed Successfully"
        )