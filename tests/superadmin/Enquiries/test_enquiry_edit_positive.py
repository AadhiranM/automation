import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_edit_page import SAEnquiryEditPage


@pytest.mark.superadmin
class TestEnquiryEditPositive:

    def test_edit_status_success(self, setup):
        list_page = SAEnquiryListPage(setup)

        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_edit()

        edit = SAEnquiryEditPage(setup)

        # Step 1: Button must be disabled at start
        assert not edit.is_submit_enabled(), "Submit should be disabled before any changes."

        # Step 2: Change status
        edit.change_status("New")

        # Step 3: Button must now be enabled
        assert edit.is_submit_enabled(), "Submit button is not enabled after selecting status!"

        # Step 4: Save
        edit.click_save()

        # Step 5: Validate popup
        edit.wait_success()

        print("✔ Status updated successfully.")
