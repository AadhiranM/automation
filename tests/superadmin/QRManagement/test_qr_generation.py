import pytest
import time
from selenium.webdriver.common.by import By
from pages.superadmin.QRManagement.sa_qr_generation_page import SAQRGenerationPage
from pages.superadmin.QRManagement.sa_qr_list_page import SAQRListPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestQRGeneration:

    def test_generate_qr_success(self, login_superadmin):

        driver = login_superadmin["driver"]

        qr = SAQRGenerationPage(driver)

        # =====================================================
        # STEP 1 - OPEN PAGE
        # =====================================================

        qr.goto_page()
        qr.wait_for_page()

        # =====================================================
        # STEP 2 - MANUFACTURER
        # =====================================================

        qr.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")

        # wait dropdown stabilize
        time.sleep(1)

        # =====================================================
        # STEP 3 - PRODUCT ID
        # =====================================================

        qr.select_product_id("M19285")

        # wait dependent dropdown load
        time.sleep(2)

        # =====================================================
        # STEP 4 - BATCH
        # =====================================================

        unique_id = str(int(time.time()))[-9:]

        qr.enter_batch(unique_id)

        # =====================================================
        # STEP 5 - VARIANT SKU
        # =====================================================

        qr.select_variant_sku()

        # wait variant load complete
        time.sleep(1)

        # =====================================================
        # STEP 6 - QUANTITY
        # =====================================================

        qr.enter_quantity("10")

        # =====================================================
        # STEP 7 - DATES
        # =====================================================

        qr.select_mfg_date("2026-05-08")

        time.sleep(1)

        qr.select_expiry_date("2026-05-12")

        # 🔥 IMPORTANT
        # close flatpickr overlay
        qr.close_calendar_overlay()

        time.sleep(1)

        # =====================================================
        # STEP 8 - BATCH LOCATION
        # =====================================================

        qr.select_batch_location("Chennai")

        time.sleep(1)

        # =====================================================
        # STEP 9 - DROPDOWNS
        # =====================================================

        qr.select_dimension("1 cm")

        time.sleep(1)

        qr.select_qr_type(
            "QR code with microtext and no invisible text"
        )

        time.sleep(1)

        qr.select_image_format("SVG")

        time.sleep(1)

        # =====================================================
        # STEP 10 - GENERATE QR
        # =====================================================

        qr.click_generate()

        # =====================================================
        # SUCCESS TOAST WAIT
        # =====================================================

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'toast')]")
            )
        )

        # backend save wait
        time.sleep(5)

        # =====================================================
        # STEP 11 - VALIDATION
        # =====================================================

        qr_list = SAQRListPage(driver)

        qr_list.goto_page()

        # wait table load
        time.sleep(3)

        # =====================================================
        # GET LATEST BATCH
        # =====================================================

        latest_batch = qr_list.get_first_batch_text()

        print("Latest Batch:", latest_batch)

        # backend removes first digit
        expected_batch = unique_id[1:]

        print("Expected Batch:", expected_batch)

        assert expected_batch in latest_batch, \
            f"Generated batch not found. Expected: {expected_batch}, Actual: {latest_batch}"

        print("QR Batch Validation Passed")