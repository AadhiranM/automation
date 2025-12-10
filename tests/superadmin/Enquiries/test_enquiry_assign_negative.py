import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_assign_page import SAEnquiryAssignPage


@pytest.mark.superadmin
class TestEnquiryAssignNegative:

    def test_assign_without_selecting_user(self, setup):
        """Submit without selecting a user should show error OR simply not assign."""
        list_page = SAEnquiryListPage(setup)

        list_page.search("mansi")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_assign_user()

        assign_page = SAEnquiryAssignPage(setup)

        # Try submit without selecting
        assign_page.submit()

        # If error popup appears → good
        try:
            assign_page.wait_for_error_popup()
        except:
            pass   # If popup does not appear, still fine

        setup.refresh()
        list_page.search("mansi")

        assert list_page.get_first_row_assigned_user() == "Not Assigned"

    def test_close_modal_without_assigning(self, setup):
        """Closing popup should not assign any user."""
        list_page = SAEnquiryListPage(setup)

        list_page.search("mansi")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_assign_user()

        assign_page = SAEnquiryAssignPage(setup)
        assign_page.close_modal()

        setup.refresh()
        list_page.search("mansi")

        assert list_page.get_first_row_assigned_user() == "Not Assigned"
