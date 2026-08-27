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
class TestQRReassign:

    def test_reassign_completed_qr(self, setup):

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
            f"REASSIGN TEST BATCH : [{batch_no}]"
        )
        print("=" * 60)

        # =====================================================
        # STEP 2 - OPEN QR LIST
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

        # =====================================================
        # STEP 4 - READ CURRENT PRODUCT + VARIANT
        # =====================================================

        current_product, current_variant = (
            qr_list.get_batch_product_and_variant(
                batch_no
            )
        )

        print(
            f"Current Product : {current_product}"
        )

        print(
            f"Current Variant : {current_variant}"
        )

        # =====================================================
        # STEP 5 - OPEN THREE-DOT ACTION MENU
        #         AND OPEN REASSIGN MODAL
        # =====================================================

        qr_list.open_reassign_modal(
            batch_no
        )

        # =====================================================
        # STEP 6 - SELECT DIFFERENT PRODUCT + VARIANT
        # =====================================================

        new_product, new_variant = (
            qr_list.get_different_product_and_variant(
                current_product,
                current_variant
            )
        )

        print(
            f"New Product     : {new_product}"
        )

        print(
            f"New Variant     : {new_variant}"
        )

        # =====================================================
        # STEP 7 - SUBMIT REASSIGN
        # =====================================================

        qr_list.reassign_qr(
            batch_no,
            new_product,
            new_variant
        )

        # =====================================================
        # STEP 8 - SEARCH BATCH AGAIN
        # =====================================================

        qr_list.search_batch(
            batch_no
        )

        qr_list.wait_for_batch(
            batch_no
        )

        # =====================================================
        # STEP 9 - READ UPDATED PRODUCT + VARIANT
        # =====================================================

        actual_product, actual_variant = (
            qr_list.get_batch_product_and_variant(
                batch_no
            )
        )

        print(
            f"Updated Product : {actual_product}"
        )

        print(
            f"Updated Variant : {actual_variant}"
        )

        # =====================================================
        # STEP 10 - VALIDATE PRODUCT
        # =====================================================

        assert actual_product == new_product, (
            f"Product was not reassigned correctly. "
            f"Expected: {new_product} | "
            f"Actual: {actual_product}"
        )

        # =====================================================
        # STEP 11 - VALIDATE VARIANT
        # =====================================================

        assert actual_variant == new_variant, (
            f"Variant was not reassigned correctly. "
            f"Expected: {new_variant} | "
            f"Actual: {actual_variant}"
        )

        # =====================================================
        # FINAL RESULT
        # =====================================================

        print("=" * 60)
        print(
            f"REASSIGN VALIDATION PASSED : [{batch_no}]"
        )
        print(
            f"Old Product : {current_product}"
        )
        print(
            f"New Product : {actual_product}"
        )
        print(
            f"Old Variant : {current_variant}"
        )
        print(
            f"New Variant : {actual_variant}"
        )
        print("=" * 60)