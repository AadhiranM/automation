import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_sendemail_page import SAEnquirySendEmailPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestSendEmailPositive:

    def test_send_email(self, setup):
        list_page = SAEnquiryListPage(setup)
        email_page = SAEnquirySendEmailPage(setup)

        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        email_page.type_subject("Test Subject")
        email_page.type_body("Test Email Body")
        email_page.click_send()

        #  Wait + validate toast
        email_page.get_toast_text()
        toast_text = email_page.get_toast_text()

        assert toast_text == "Email sent successfully!", \
            f"Toast mismatch: {toast_text}"

        print("✔ Email sent successfully toast validated")


    def test_send_email_and_verify_history(self, setup):
        SUBJECT_TEXT = "Automation Email Subject"
        BODY_TEXT = "This is an automated test email body."

        list_page = SAEnquiryListPage(setup)
        email_page = SAEnquirySendEmailPage(setup)

        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        # Email field disabled
        assert email_page.is_email_disabled(), "Email field should be disabled"

        # Previous Email section visible
        assert email_page.is_previous_email_section_present(), \
            "Previous Email section is missing"

        # Send email
        email_page.type_subject(SUBJECT_TEXT)
        email_page.type_body(BODY_TEXT)
        email_page.click_send()
        email_page.get_toast_text()

        #  Verify latest email
        details = email_page.get_previous_email_details()
        assert SUBJECT_TEXT in details["subject"], "Subject mismatch"
        assert details["body"] == BODY_TEXT, "Body mismatch"
        assert "Superadmin" in details["sender"], "Sender mismatch"

        # Verify latest email content
        details = email_page.get_previous_email_details()

        assert SUBJECT_TEXT in details["subject"], "Subject mismatch"
        assert details["body"] == BODY_TEXT, "Body mismatch"

        #  Validate ONLY current sender
        assert "Superadmin" in details["sender"], \
            f"Latest email sender mismatch: {details['sender']}"

        #  Verify date format only
        dates = email_page.get_all_previous_dates()
        for d in dates:
            assert email_page.is_valid_date_format(d), \
                f"Invalid date format: {d}"

        print("✔ Email sent & history validated successfully")
