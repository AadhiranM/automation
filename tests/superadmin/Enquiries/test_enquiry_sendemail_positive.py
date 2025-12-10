import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_sendemail_page import SAEnquirySendEmailPage


@pytest.mark.superadmin
class TestSendEmailPositive:

    def test_send_email(self, setup):
        list_page = SAEnquiryListPage(setup)

        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        email = SAEnquirySendEmailPage(setup)

        email.type_subject("Test Subject")
        email.type_body("Test Email Body")
        email.click_send()

        email.wait_for_toast()
        print("✔ Email sent successfully.")

    def test_send_email_and_verify_history(self, setup):

        SUBJECT_TEXT = "Automation Email Subject"
        BODY_TEXT = "This is an automated test email body."

        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        email = SAEnquirySendEmailPage(setup)

        email.type_subject(SUBJECT_TEXT)
        email.type_body(BODY_TEXT)
        email.click_send()

        email.wait_for_toast()

        details = email.get_previous_email_details()

        assert details["subject"] == SUBJECT_TEXT, "❌ Subject mismatch"
        assert details["body"] == BODY_TEXT, "❌ Body text mismatch"
        assert "Superadmin" in details["sender"], "❌ Sender mismatch"

        print("✔ Email history updated correctly:", details)
