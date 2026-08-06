import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_assign_page import (
    SAEnquiryAssignPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryAssignUnassignPositive:

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_assign_internal_user(self, setup):

        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        list_page.goto_page()

        current_user = (
            assign_page.get_first_row_assigned_user()
        )

        if current_user.lower() == "not assigned":

            selected_user = (
                assign_page.assign_first_internal_user()
            )

            actual_user = (
                assign_page.get_first_row_assigned_user()
            )

            assert actual_user == selected_user

        else:

            print(
                f"Already assigned to {current_user}"
            )

            assert current_user != "Not Assigned"

    # =====================================================

    @pytest.mark.sanity
    def test_unassign_internal_user(self, setup):

        list_page = SAEnquiryListPage(setup)
        assign_page = SAEnquiryAssignPage(setup)

        list_page.goto_page()

        current_user = (
            assign_page.get_first_row_assigned_user()
        )

        if current_user.lower() != "not assigned":

            assign_page.unassign_internal_user()

            assert (
                assign_page.get_first_row_assigned_user()
                == "Not Assigned"
            )

        else:

            print(
                "Already unassigned"
            )

            assert (
                assign_page.get_first_row_assigned_user()
                == "Not Assigned"
            )