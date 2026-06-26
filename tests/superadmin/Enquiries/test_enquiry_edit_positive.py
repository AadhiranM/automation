import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_edit_page import (
    SAEnquiryEditPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryEditPositive:


    def test_edit_status_success(
            self,
            setup
    ):

        list_page = SAEnquiryListPage(setup)

        list_page.goto_page()

        enquiry_name = (
            list_page.get_first_row_name()
        )

        old_status = (
            list_page.get_first_row_status()
        )


        list_page.click_edit()

        edit_page = (
            SAEnquiryEditPage(setup)
        )

        edit_page.wait_until_loaded()

        new_status = (
            edit_page.get_next_status()
        )

        edit_page.change_status(
            new_status
        )

        assert (
            edit_page.is_submit_enabled()
        )

        edit_page.click_save()

        edit_page.wait_success()

        list_page.goto_page()

        list_page.search(
            enquiry_name
        )

        updated_status = (
            list_page.get_first_row_status()
        )

        assert (
            updated_status
            ==
            new_status
        ), (
            f"Expected {new_status}, "
            f"but got {updated_status}"
        )