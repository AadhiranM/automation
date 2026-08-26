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
class TestQRCancelRequest:

    def test_cancel_completed_qr(self, setup):
        qr_list = SAQRListPage(setup)

        helper = TestQRGeneration()

        # ==========================================
        # STEP 1 - CREATE FRESH COMPLETED BATCH
        # ==========================================

        batch_no = helper.create_fresh_completed_batch(setup)

        print("=" * 60)
        print(f"CANCEL TEST BATCH : [{batch_no}]")
        print("=" * 60)

        # ==========================================
        # STEP 2 - CANCEL REQUEST
        # ==========================================

        qr_list.cancel_request(
            batch_no,
            "Automation validation - Cancel Request"
        )

        # ==========================================
        # STEP 3 - VALIDATE CANCELLED STATUS
        # ==========================================

        qr_list.search_batch(batch_no)

        qr_list.wait_for_batch(batch_no)

        qr_list.verify_batch_status(
            batch_no,
            "Request Cancelled"
        )

        print(
            f"Cancel Request validation passed: "
            f"{batch_no}"
        )