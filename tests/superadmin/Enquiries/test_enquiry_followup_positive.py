import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_followup_page import SAEnquiryFollowUpPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestFollowUpPositive:

    def test_add_followup_success(self, setup):
        list_page = SAEnquiryListPage(setup)

        # Navigate to Enquiries
        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_follow_up()

        followup_page = SAEnquiryFollowUpPage(setup)

        message = "Automation follow-up message"

        # Add follow-up
        followup_page.type_followup(message)
        followup_page.click_submit()

        # Validate toast
        toast_text = followup_page.get_toast_text()
        assert "success" in toast_text.lower(), \
            f"Unexpected toast message: {toast_text}"

        # Validate latest follow-up history
        details = followup_page.get_latest_followup()

        assert details["message"] == message, "Follow-up message mismatch"
        assert "Superadmin" in details["sender"], "Sender mismatch"
        assert details["time"] != "", "Timestamp missing"

        print("✔ Follow-up added and verified successfully")
