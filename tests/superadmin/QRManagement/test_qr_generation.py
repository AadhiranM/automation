import pytest
from pages.superadmin.QRManagement.sa_qr_generation_page import SAQRGenerationPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestQRGeneration:

    def test_generate_qr_success(self, login_superadmin):
        driver = login_superadmin["driver"]

        qr_page = SAQRGenerationPage(driver)

        qr_page.goto_page()
        qr_page.wait_for_page()

        qr_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        qr_page.select_product_id("M19285")

        qr_page.wait_for_product_autofill()

        qr_page.enter_batch("B19285-45154545")
        qr_page.enter_quantity("10")

        qr_page.select_variant_sku("M19285")

        qr_page.select_mfg_date("2026-04-30")
        qr_page.select_expiry_date("2026-05-09")

        qr_page.select_dimension("1 cm")
        qr_page.select_batch_location("Chennai")
        qr_page.select_qr_type("QR")
        qr_page.select_image_format("SVG")

        qr_page.click_generate()

        assert qr_page.is_qr_generated()