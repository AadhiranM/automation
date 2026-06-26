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

    def test_view_enquiry(self, setup):

        list_page = SAEnquiryListPage(setup)

        view_page = SAEnquiryViewPage(setup)

        list_page.goto_page()

        expected_id = (
            list_page.get_first_row_id()
        )

        list_page.click_view()

        assert (
            view_page.is_view_page_opened(
                expected_id
            )
        ), (
            f"Expected URL to contain '/{expected_id}/show', "
            f"but got '{setup.current_url}'"
        )