import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_followup_page import (
    SAEnquiryFollowUpPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestFollowUpNegative:

    @pytest.mark.sanity
    def test_add_followup_without_message(
            self,
            setup
    ):

        list_page = SAEnquiryListPage(setup)

        followup_page = SAEnquiryFollowUpPage(setup)

        list_page.goto_page()

        enquiry_name = (
            list_page.get_first_row_name()
        )

        list_page.search(
            enquiry_name
        )

        list_page.wait_for_results()

        list_page.click_follow_up()

        # -------------------------------------------------
        # Do NOT enter any Follow-up Message
        # Directly click Submit
        # -------------------------------------------------

        followup_page.click_submit()

        print(
            "Submit clicked without Follow-up Message"
        )

        # -------------------------------------------------
        # Verify Message validation
        # -------------------------------------------------

        assert (
            followup_page.wait_for_content_error()
        ), "Message content validation message is not displayed"

        print(
            "PASS: Message content validation message displayed"
        )