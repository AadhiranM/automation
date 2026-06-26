import time
import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_sendemail_page import (
    SAEnquirySendEmailPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestSendEmailPositive:

    def test_send_email_and_verify_history(
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

        subject = (
            f"Automation Subject {int(time.time())}"
        )

        body = (
            f"Automation Email Body {int(time.time())}"
        )

        toast = email_page.send_email(
            subject,
            body
        )

        assert (
            "successfully"
            in
            toast.lower()
        )

        # Verify newly sent email appears at top
        details = (
            email_page.get_previous_email_details()
        )

        assert (
            subject
            in
            details["subject"]
        ), (
            f"Subject not found. "
            f"Expected: {subject}, "
            f"Actual: {details['subject']}"
        )

        print(
            "✔ Email sent successfully and displayed in Previous Email history"
        )