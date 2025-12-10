import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_assign_page import SAEnquiryAssignPage


@pytest.mark.superadmin
class TestEnquiryAssignPositive:

    def test_assign_internal_user(self, setup):
        list_page = SAEnquiryListPage(setup)

        list_page.search("mansi")
        list_page.wait_first_row_loaded()
        list_page.open_action_menu()
        list_page.click_assign_user()

        assign_page = SAEnquiryAssignPage(setup)
        assign_page.assign_user("sara")

        # Refresh and validate assigned user
        setup.refresh()
        list_page.search("mansi")

        assigned = list_page.get_first_row_assigned_user()
        assert assigned == "sara", f"Expected 'sara', got '{assigned}'"
