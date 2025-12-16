import pytest
from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage
from pages.superadmin.Enquiries.sa_enquiry_assign_page import SAEnquiryAssignPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryAssignUnassignPositive:

    def test_assign_internal_user_success(self, setup):
        """
        Verify internal user can be assigned successfully
        """

        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        # 1️⃣ Go to enquiry list and search
        list_page.goto_page()
        list_page.search("mansi")
        assert list_page.is_row_present(), "No enquiry found for mansi"

        # 2️⃣ Assign internal user
        assign_page.open_actions()
        assign_page.open_assign_user()
        assign_page.choose_internal_user("Sunio Soni")
        assign_page.submit_assign_user()
        assign_page.confirm_assign_success()

        # 3️⃣ Refresh list and verify assignment
        list_page.goto_page()
        list_page.search("mansi")

        assert assign_page.assigned_user_value() == "Sunio Soni"

    def test_unassign_internal_user_success(self, setup):
        """
        Verify internal user can be un-assigned successfully
        """

        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        # 1️⃣ Go to enquiry list
        list_page.goto_page()
        list_page.search("mansi")

        # 2️⃣ Ensure user is already assigned (state-safe)
        assign_page.ensure_user_assigned("Sunio Soni")

        # 3️⃣ Un-assign user
        assign_page.open_actions()
        assign_page.click_unassign()
        assign_page.confirm_unassign_yes()
        assign_page.confirm_unassign_success()

        # 4️⃣ Wait until table updates
        assign_page.wait_until_unassigned()

        # 5️⃣ Verify un-assigned status
        list_page.goto_page()
        list_page.search("mansi")

        assert assign_page.assigned_user_value() == "Not Assigned"

    def test_unassign_cancel_should_not_change_user(self, setup):
        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        list_page.goto_page()
        list_page.search("mansi")

        # STEP 1: Ensure assigned (mandatory)
        if assign_page.assigned_user_value().strip() == "Not Assigned":
            assign_page.open_actions()
            assign_page.open_assign_user()
            assign_page.choose_internal_user("Sunio Soni")
            assign_page.submit_assign_user()
            assign_page.confirm_assign_success()

            list_page.goto_page()
            list_page.search("mansi")

        assigned_before = assign_page.assigned_user_value().strip()
        assert assigned_before == "Sunio Soni"

        # STEP 2: Try un-assign
        assign_page.open_actions()
        unassign_available = assign_page.click_unassign()

        # If un-assign not visible → FAIL CLEARLY
        assert unassign_available, "Un-assign option not available even after assignment"

        assign_page.confirm_unassign_cancel()

        # STEP 3: Verify user still assigned
        list_page.goto_page()
        list_page.search("mansi")

        assert assign_page.assigned_user_value().strip() == assigned_before
