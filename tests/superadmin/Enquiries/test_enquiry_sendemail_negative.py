import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_sendemail_page import SAEnquirySendEmailPage


@pytest.mark.superadmin
class TestSendEmailNegative:

    def test_blank_subject(self, setup):
        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        email = SAEnquirySendEmailPage(setup)

        email.type_body("Testing body only")
        email.click_send()

        assert email.wait_subject_error(), "❌ Subject error message not shown"
        print("✔ Blank subject validation displayed.")


    def test_blank_body(self, setup):
        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        email = SAEnquirySendEmailPage(setup)

        email.type_subject("Subject only")
        email.click_send()

        assert email.wait_body_error(), "❌ Body error message not shown"
        print("✔ Blank body validation displayed.")


    def test_close_without_sending(self, setup):
        list_page = SAEnquiryListPage(setup)
        list_page.search("test")
        list_page.open_action_menu()
        list_page.click_send_email()

        # Browser back to close modal
        setup.back()

        assert "enquiries" in setup.current_url.lower(), "❌ Did not return to enquiries page"
        print("✔ Close without sending returned to list page.")
