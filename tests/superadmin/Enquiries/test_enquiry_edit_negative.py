import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_edit_page import SAEnquiryEditPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryEditNegative:

    def test_submit_disabled_without_change(self, setup):
        list_page = SAEnquiryListPage(setup)
        list_page.goto_page()

        list_page.search("test")
        list_page.open_action_menu()
        list_page.click_edit()

        edit = SAEnquiryEditPage(setup)
        current = edit.get_current_status()

        edit.change_status(current)

        assert not edit.is_submit_enabled()
