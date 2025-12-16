import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_sendemail_page import SAEnquirySendEmailPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")  #  login handled
class TestSendEmailNegative:

    def test_send_email_blank_subject(self, setup):
        list_page = SAEnquiryListPage(setup)
        email_page = SAEnquirySendEmailPage(setup)

        #  Navigate to Enquiries
        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        #  Only body filled
        email_page.type_body("Testing body only")
        email_page.click_send()

        # Validate subject error
        assert email_page.wait_subject_error(), \
            "Subject validation error not shown"

        print(" Blank subject validation displayed")


    def test_send_email_blank_body(self, setup):
        list_page = SAEnquiryListPage(setup)
        email_page = SAEnquirySendEmailPage(setup)

        #  Navigate to Enquiries
        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        #  Only subject filled
        email_page.type_subject("Subject only")
        email_page.click_send()

        #  Validate body error
        assert email_page.wait_body_error(), \
            "Body validation error not shown"

        print(" Blank body validation displayed")


    def test_send_email_without_subject_and_body(self, setup):
        list_page = SAEnquiryListPage(setup)
        email_page = SAEnquirySendEmailPage(setup)

        #  Navigate to Enquiries
        list_page.goto_page()
        list_page.search("test")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_send_email()

        #  Click send without filling anything
        email_page.click_send()

        #  Both validations must appear
        assert email_page.wait_subject_error(), \
            "Subject validation error not shown"
        assert email_page.wait_body_error(), \
            "Body validation error not shown"

        print(" Blank subject & body validation displayed")
