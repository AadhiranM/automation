import os

import pytest

from pages.superadmin.QRManagement.sa_product_import_page import (
    SAProductImportPage
)
from pages.superadmin.QRManagement.sa_product_import_page import (
    SAProductImportPage,
    INVALID_IMAGE_FILE,
    INVALID_PDF_FILE
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestProductImportNegative:

    # =========================================================
    # INVALID IMAGE FILE - JPEG
    # =========================================================

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_import_product_with_jpeg_file_should_fail(
            self,
            login_superadmin
    ):
        driver = login_superadmin["driver"]
        page = SAProductImportPage(driver)

        page.goto_product_page()

        manufacturer_name = (
            page.get_first_manufacturer()
        )

        print(
            f"First Manufacturer: {manufacturer_name}"
        )

        page.open_import()

        page.click_continue()

        page.upload_invalid_product_file(
            INVALID_IMAGE_FILE
        )

        page.select_manufacturer(
            manufacturer_name
        )

        page.click_import()

        error_message = (
            page.get_invalid_file_message()
        )

        expected_message = (
            "Invalid file format. "
            "Please upload an Excel (.xlsx) file only."
        )

        assert expected_message in error_message, (
            f"Unexpected validation message: "
            f"{error_message}"
        )


    # =========================================================
    # INVALID PDF FILE
    # =========================================================

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_import_product_with_pdf_file_should_fail(
            self,
            login_superadmin
    ):
        driver = login_superadmin["driver"]
        page = SAProductImportPage(driver)

        page.goto_product_page()

        manufacturer_name = (
            page.get_first_manufacturer()
        )

        print(
            f"First Manufacturer: {manufacturer_name}"
        )

        page.open_import()

        page.click_continue()

        page.upload_invalid_product_file(
            INVALID_PDF_FILE
        )

        page.select_manufacturer(
            manufacturer_name
        )

        page.click_import()

        error_message = (
            page.get_invalid_file_message()
        )

        expected_message = (
            "Invalid file format. "
            "Please upload an Excel (.xlsx) file only."
        )

        assert expected_message in error_message, (
            f"Unexpected validation message: "
            f"{error_message}"
        )