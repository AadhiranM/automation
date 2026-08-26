import pytest

from pages.superadmin.QRManagement.sa_qr_list_page import (
    SAQRListPage
)

from tests.superadmin.QRManagement.test_qr_generation import (
    TestQRGeneration
)


@pytest.mark.superadmin
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestQRInvalidate:

    def test_invalidate_completed_qr(
        self,
        login_superadmin
    ):

        driver = login_superadmin["driver"]

        # =====================================================
        # STEP 1 - CREATE FRESH COMPLETED BATCH
        # =====================================================

        helper = TestQRGeneration()

        batch_no = (
            helper.create_fresh_completed_batch(
                driver
            )
        )

        print(
            "Invalidate test batch:",
            batch_no
        )

        # =====================================================
        # STEP 2 - OPEN QR LIST
        # =====================================================

        qr_list = SAQRListPage(driver)

        qr_list.goto_page()
        qr_list.wait_for_page()

        qr_list.search_batch(
            batch_no
        )

        qr_list.wait_for_batch(
            batch_no
        )

        # =====================================================
        # STEP 3 - INVALIDATE
        # =====================================================

        qr_list.invalidate_qr(
            batch_no,
            "Automation validation - Invalidate QR"
        )

        # =====================================================
        # STEP 4 - VALIDATE
        # =====================================================

        qr_list.wait_for_batch_status(
            batch_no,
            "QR Invalidated"
        )

        qr_list.verify_batch_status(
            batch_no,
            "QR Invalidated"
        )

        print(
            "Invalidate validation PASSED"
        )