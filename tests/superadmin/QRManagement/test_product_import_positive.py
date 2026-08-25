import pytest

from pages.superadmin.QRManagement.sa_product_import_page import (
    SAProductImportPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestProductImportPositive:

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_import_product_excel_successfully(
            self,
            login_superadmin
    ):

        driver = login_superadmin["driver"]

        page = SAProductImportPage(driver)

        # =====================================================
        # STEP 1 - OPEN PRODUCT LIST
        # =====================================================

        page.goto_product_page()

        # =====================================================
        # STEP 2 - GET FIRST MANUFACTURER
        # =====================================================

        manufacturer_name = (
            page.get_first_manufacturer()
        )

        print(
            f"First Manufacturer: "
            f"{manufacturer_name}"
        )

        # =====================================================
        # STEP 3 - CLICK IMPORT
        # =====================================================

        page.open_import()

        # =====================================================
        # STEP 4 - CONTINUE
        # =====================================================

        page.click_continue()

        # =====================================================
        # STEP 5 - UPLOAD EXCEL
        # =====================================================

        page.upload_product_excel()

        # =====================================================
        # STEP 6 - SELECT MANUFACTURER
        # =====================================================

        page.select_manufacturer(
            manufacturer_name
        )
        # input("\nPAUSED - Run the DevTools commands, then press ENTER...\n")

        # =====================================================
        # STEP 7 - IMPORT
        # =====================================================

        page.click_import()

        # =====================================================
        # STEP 8 - VERIFY TOAST
        # =====================================================

        # =====================================================
        # STEP 8 - VERIFY TOAST
        # =====================================================

        toast_message = page.get_toast_message()

        # Remove toast close icon if it is included in .text
        toast_message = toast_message.replace("✖", "").strip()

        expected_message = (
            "Product import initiated successfully."
        )

        assert toast_message == expected_message, (
            f"Unexpected toast message: {toast_message}"
        )

        # =====================================================
        # STEP 9 - WAIT FOR IMPORT LOGS
        # =====================================================

        page.wait_for_import_logs()

        # =====================================================
        # STEP 10 - VERIFY IMPORT SUCCESS
        # =====================================================

        assert page.wait_until_import_success(), (
            "Product import did not reach Success status. "
            f"Final status: "
            f"{page.get_first_import_status()}"
        )

        # =====================================================
        # STEP 11 - DOWNLOAD UPLOADED FILE
        # =====================================================

        page.download_uploaded_file()