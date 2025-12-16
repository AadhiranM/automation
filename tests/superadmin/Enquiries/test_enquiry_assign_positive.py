import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_assign_page import SAEnquiryAssignPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryAssignUnassignPositive:

    def test_assign_internal_user_success(self, setup):
        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        list_page.goto_page()
        list_page.search("mansi")
        assert list_page.is_row_present(), "No enquiry found for mansi"

        assign_page.open_actions()
        assign_page.open_assign_user()
        assign_page.choose_internal_user("Sunio Soni")
        assign_page.submit_assign_user()
        assign_page.confirm_assign_success()

        # ✅ WAIT for UI update
        assign_page.wait_until_assigned_user_is("Sunio Soni")

        assert assign_page.assigned_user_value().strip() == "Sunio Soni"

    def test_unassign_internal_user_success(self, setup):
        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        list_page.goto_page()
        list_page.search("Django")

        # ✅ Ensure precondition: assigned
        if assign_page.assigned_user_value().strip() != "Sunio Soni":
            assign_page.open_actions()
            assign_page.open_assign_user()
            assign_page.choose_internal_user("Sunio Soni")
            assign_page.submit_assign_user()
            assign_page.confirm_assign_success()
            assign_page.wait_until_assigned_user_is("Sunio Soni")

        # ✅ Unassign
        assign_page.open_actions()
        assign_page.click_unassign()
        assign_page.confirm_unassign_yes()
        assign_page.confirm_unassign_success()

        # ✅ WAIT for UI update
        assign_page.wait_until_assigned_user_is("Not Assigned")

        assert assign_page.assigned_user_value().strip() == "Not Assigned"

    def test_unassign_cancel_should_not_change_user(self, setup):
        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        list_page.goto_page()
        list_page.search("Appium")

        # ✅ Ensure precondition: assigned
        if assign_page.assigned_user_value().strip() != "fgfd":
            assign_page.open_actions()
            assign_page.open_assign_user()
            assign_page.choose_internal_user("fgfd")
            assign_page.submit_assign_user()
            assign_page.confirm_assign_success()
            assign_page.wait_until_assigned_user_is("fgfd")

        assigned_before = assign_page.assigned_user_value().strip()
        assert assigned_before == "fgfd"

        # ✅ Cancel unassign
        assign_page.open_actions()
        assign_page.click_unassign()
        assign_page.confirm_unassign_cancel()

        # ✅ Verify user not changed
        assign_page.wait_until_assigned_user_is("fgfd")

        assert assign_page.assigned_user_value().strip() == assigned_before
