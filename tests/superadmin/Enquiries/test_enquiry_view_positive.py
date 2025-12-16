import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_view_page import SAEnquiryViewPage

@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryViewPositive:

    def test_view_enquiry_details(self, setup):
        list_page = SAEnquiryListPage(setup)

        # ⭐ NEW — Open Enquiry list directly (no menu click)
        list_page.goto_page()

        list_page.search("test")
        list_page.open_action_menu()
        list_page.click_view()

        view = SAEnquiryViewPage(setup)
        view.wait_until_loaded()

        assert view.is_visible(view.NAME)
        assert view.is_visible(view.EMAIL)
        assert view.is_visible(view.MESSAGE)
        assert view.is_visible(view.STATUS)
