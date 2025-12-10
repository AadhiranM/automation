import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_followup_page import SAEnquiryFollowUpPage


@pytest.mark.usefixtures("login_superadmin")
@pytest.mark.superadmin
class TestFollowUpPositive:

    def test_add_followup_success(self, setup):
        """Add follow-up → toast appears → history updated"""

        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_follow_up()

        follow = SAEnquiryFollowUpPage(setup)

        message = "Automation follow-up message"
        follow.type_followup(message)
        follow.click_submit()

        # Wait for toast
        follow.wait_for_success()

        # Validate latest follow-up
        details = follow.get_latest_followup()

        assert details["message"] == message, "Message mismatch"
        assert "Superadmin" in details["sender"], "Sender incorrect"
        assert details["time"] != "", "Timestamp missing"

        print("✔ Follow-up added and verified successfully")
