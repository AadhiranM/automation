import time
import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_followup_page import (
    SAEnquiryFollowUpPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestFollowUpPositive:

    def test_add_followup_success(
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

        list_page.open_first_row_actions()

        list_page.click_follow_up()

        message = (
            f"Automation Follow Up {int(time.time())}"
        )

        followup_page.type_followup(
            message
        )

        followup_page.click_submit()

        followup_page.wait_for_followup_refresh(
            message
        )

        assert (
            followup_page.latest_followup_contains(
                message
            )
        ), (
            f"Follow-up message not found: {message}"
        )

        print(
            "✔ Follow-up submitted and displayed in Previous Follow-ups"
        )