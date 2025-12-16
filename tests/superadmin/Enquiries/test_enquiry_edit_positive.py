import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_edit_page import SAEnquiryEditPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryEditPositive:

    def test_edit_status_success(self, setup):
        list_page = SAEnquiryListPage(setup)
        list_page.goto_page()

        # Step 1: Search the enquiry
        list_page.search("test")
        list_page.open_action_menu()
        list_page.click_edit()

        edit = SAEnquiryEditPage(setup)

        # Step 2: Choose a different status
        current = edit.get_current_status()

        all_status = ["New", "Contacted", "Demo Scheduled", "Onboarded", "Rejected"]
        new_status = [s for s in all_status if s != current][0]

        edit.change_status(new_status)
        assert edit.is_submit_enabled(), "Submit should enable after change"

        # Step 3: Save
        edit.click_save()
        edit.wait_success()

        # Step 4: Return to list page and verify status directly from table
        list_page.goto_page()
        list_page.search("test")

        displayed_status = list_page.get_first_row_status()
        assert displayed_status == new_status, f"Status not updated in list. Expected: {new_status}, Got: {displayed_status}"
