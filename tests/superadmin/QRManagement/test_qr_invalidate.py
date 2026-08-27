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

    def test_invalidate_completed_qr(self, setup):

        qr_list = SAQRListPage(setup)

        helper = TestQRGeneration()

        # ==========================================
        # STEP 1 - CREATE FRESH COMPLETED BATCH
        # ==========================================

        batch_no = helper.create_fresh_completed_batch(
            setup
        )

        print("=" * 60)
        print(
            f"INVALIDATE TEST BATCH : [{batch_no}]"
        )
        print("=" * 60)

        # ==========================================
        # STEP 2 - INVALIDATE QR
        # ==========================================

        qr_list.invalidate_qr(
            batch_no,
            "Automation validation - Invalidate QR"
        )

        # ==========================================
        # STEP 3 - VALIDATE INVALIDATED STATUS
        # ==========================================

        qr_list.search_batch(
            batch_no
        )

        qr_list.wait_for_batch(
            batch_no
        )

        qr_list.verify_batch_status(
            batch_no,
            "QR Invalidated"
        )

        print(
            f"Invalidate validation passed: "
            f"{batch_no}"
        )