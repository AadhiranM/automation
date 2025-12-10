import pytest
from selenium.common.exceptions import TimeoutException

from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_followup_page import SAEnquiryFollowUpPage


@pytest.mark.usefixtures("login_superadmin")
@pytest.mark.superadmin
class TestFollowUpNegative:

    def test_followup_empty_message(self, setup):
        """Submitting empty follow-up should NOT show success toast."""

        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_follow_up()

        follow = SAEnquiryFollowUpPage(setup)

        follow.click_submit()

        # Assert → NO toast should appear
        with pytest.raises(TimeoutException):
            follow.wait_for_success()

        print("✔ Empty follow-up rejected (no toast).")

    def test_followup_whitespace_only(self, setup):
        """Whitespace-only follow-up must be rejected."""

        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_follow_up()

        follow = SAEnquiryFollowUpPage(setup)

        follow.type_followup("   ")  # only spaces
        follow.click_submit()

        with pytest.raises(TimeoutException):
            follow.wait_for_success()

        print("✔ Whitespace-only follow-up blocked correctly.")
