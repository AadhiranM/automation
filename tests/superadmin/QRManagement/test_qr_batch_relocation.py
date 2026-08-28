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
class TestQRBatchRelocation:

    def test_relocate_completed_qr_batch(self, setup):

        qr_list = SAQRListPage(setup)

        helper = TestQRGeneration()

        # =====================================================
        # STEP 1 - CREATE FRESH COMPLETED BATCH
        # =====================================================

        batch_no = helper.create_fresh_completed_batch(
            setup
        )

        print("=" * 60)
        print(
            f"RELOCATION TEST BATCH : [{batch_no}]"
        )
        print("=" * 60)

        # QR Generation creates the fresh batch with Chennai.
        current_location = "Chennai"

        print(
            f"Current Location : {current_location}"
        )

        # =====================================================
        # STEP 2 - OPEN QR MANAGEMENT LIST
        # =====================================================

        qr_list.goto_page()
        qr_list.wait_for_page()

        # =====================================================
        # STEP 3 - SEARCH FRESH BATCH
        # =====================================================

        qr_list.search_batch(
            batch_no
        )

        qr_list.wait_for_batch(
            batch_no
        )

        print(
            f"Batch found for relocation: {batch_no}"
        )

        # =====================================================
        # STEP 4 - OPEN THREE-DOT ACTION MENU
        #         AND UPDATE LOCATION
        # =====================================================

        qr_list.open_update_location_modal(
            batch_no
        )

        # =====================================================
        # STEP 5 - SELECT MUMBAI
        # =====================================================

        new_location = "Mumbai"

        qr_list.select_batch_location(
            new_location
        )

        print(
            f"New Location     : {new_location}"
        )

        # =====================================================
        # STEP 6 - SUBMIT LOCATION UPDATE
        # =====================================================

        qr_list.submit_location_update(
            batch_no
        )

        # =====================================================
        # STEP 7 - WAIT FOR BACKEND UPDATE
        #
        # Same synchronization approach used in Reassign and
        # QR status transitions.
        # =====================================================

        expected_location = (
            "Mumbai, Maharashtra, India"
        )

        qr_list.wait_for_location_update(
            batch_no,
            expected_location,
            timeout=60
        )

        # =====================================================
        # STEP 8 - OPEN FRESH QR MANAGEMENT LIST
        #
        # Do not validate against the old Angular/DataTables
        # row immediately after Submit.
        # =====================================================

        print(
            "Opening fresh QR Management list "
            "after location update..."
        )

        qr_list.goto_page()
        qr_list.wait_for_page()

        print(
            "Fresh QR Management list loaded"
        )

        # =====================================================
        # STEP 9 - SEARCH SAME BATCH AGAIN
        # =====================================================

        qr_list.search_batch(
            batch_no
        )

        qr_list.wait_for_batch(
            batch_no
        )

        print(
            f"Batch found again after relocation: "
            f"{batch_no}"
        )

        # =====================================================
        # STEP 10 - OPEN THREE-DOT MENU AGAIN
        # =====================================================

        qr_list.open_action_menu(
            batch_no
        )

        # =====================================================
        # STEP 11 - CLICK VIEW
        # =====================================================

        qr_list.click_action_option(
            "View"
        )

        # =====================================================
        # STEP 12 - WAIT FOR VIEW PAGE
        # =====================================================

        qr_list.wait_for_batch_view_page()

        # =====================================================
        # STEP 13 - READ UPDATED LOCATION
        # =====================================================

        actual_location = qr_list.get_batch_location_from_view()

        print(
            f"Updated Location : {actual_location}"
        )

        assert expected_location.lower() in actual_location.lower(), (
            f"Batch location was not updated correctly. "
            f"Expected: {expected_location} | "
            f"Actual: {actual_location}"
        )

        # =====================================================
        # FINAL RESULT
        # =====================================================

        print("=" * 60)
        print(
            f"BATCH RELOCATION VALIDATION PASSED : "
            f"[{batch_no}]"
        )
        print(
            f"Old Location : {current_location}"
        )
        print(
            f"New Location : {actual_location}"
        )
        print("=" * 60)
