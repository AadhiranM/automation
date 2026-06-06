import pytest

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)

from pages.superadmin.Enquiries.sa_enquiry_view_page import (
    SAEnquiryViewPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryViewPositive:

    def test_view_enquiry_details(self, setup):

        list_page = SAEnquiryListPage(setup)

        list_page.goto_page()

        expected_id = list_page.get_first_row_id()

        expected_name = (
            list_page.get_first_row_name()
        )

        expected_email = (
            list_page.get_first_row_email()
        )

        expected_company = (
            list_page.get_first_row_company()
        )

        expected_status = (
            list_page.get_first_row_status()
        )

        list_page.open_first_row_actions()

        list_page.click_view()

        view = SAEnquiryViewPage(setup)

        view.wait_until_loaded()

        actual_name = view.get_name()

        actual_email = view.get_email()

        actual_company = view.get_company()

        actual_status = view.get_status()

        assert actual_name == expected_name

        assert actual_email == expected_email

        assert actual_company == expected_company

        assert actual_status == expected_status

    def test_edit_button_visible(self, setup):

        list_page = SAEnquiryListPage(setup)

        list_page.goto_page()

        list_page.open_first_row_actions()

        list_page.click_view()

        view = SAEnquiryViewPage(setup)

        view.wait_until_loaded()

        assert view.is_visible(
            view.EDIT_BUTTON
        )