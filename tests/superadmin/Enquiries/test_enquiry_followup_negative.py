import pytest
from selenium.common.exceptions import TimeoutException
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_followup_page import SAEnquiryFollowUpPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestFollowUpNegative:

    def test_followup_empty_message(self, setup):
        """Empty follow-up should show validation error"""

        list_page = SAEnquiryListPage(setup)

        # Navigate to Enquiries
        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_follow_up()

        follow = SAEnquiryFollowUpPage(setup)

        # Submit without typing anything
        follow.click_submit()

        # ✅ Validate error message
        assert follow.wait_for_content_error(), \
            "Validation error not shown for empty follow-up"

        print("✔ Empty follow-up correctly blocked with validation error")

    def test_followup_whitespace_only(self, setup):
        """Whitespace-only follow-up should be rejected"""

        list_page = SAEnquiryListPage(setup)

        # Navigate to Enquiries
        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_follow_up()

        follow = SAEnquiryFollowUpPage(setup)

        # Enter only spaces
        follow.type_followup("   ")
        follow.click_submit()

        # ✅ Validate error message
        assert follow.wait_for_content_error(), \
            "Validation error not shown for whitespace-only follow-up"

        print("✔ Whitespace-only follow-up blocked correctly")
