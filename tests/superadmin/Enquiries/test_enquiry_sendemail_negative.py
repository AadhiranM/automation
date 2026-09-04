import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_sendemail_page import (
    SAEnquirySendEmailPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestSendEmailNegative:

    @pytest.mark.sanity
    def test_send_email_without_subject_and_message(
            self,
            setup
    ):

        list_page = SAEnquiryListPage(setup)

        email_page = SAEnquirySendEmailPage(setup)

        list_page.goto_page()

        enquiry_name = (
            list_page.get_first_row_name()
        )

        list_page.search(
            enquiry_name
        )

        list_page.wait_for_results()

        list_page.click_send_email()

        assert (
            email_page.is_email_disabled()
        )

        assert (
            email_page.is_previous_email_section_present()
        )

        # -------------------------------------------------
        # Do NOT enter Subject
        # Do NOT enter Message
        # Directly click Send
        # -------------------------------------------------

        email_page.click_send()

        print(
            "Send clicked without Subject and Message"
        )

        # -------------------------------------------------
        # Verify Subject validation
        # -------------------------------------------------

        assert (
            email_page.wait_subject_error()
        ), "Subject validation message is not displayed"

        # -------------------------------------------------
        # Verify Email Content validation
        # -------------------------------------------------

        assert (
            email_page.wait_body_error()
        ), "Email content validation message is not displayed"

        print(
            "PASS: Subject and Email content validation messages displayed"
        )