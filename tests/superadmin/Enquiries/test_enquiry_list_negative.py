import pytest
from datetime import date, timedelta

from pages.superadmin.Enquiries.sa_enquiry_list_page import (
    SAEnquiryListPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryListNegative:

    def test_search_invalid_special_characters(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.search("!@#$%^&*")

        assert page.has_no_data()

    def test_search_only_spaces(self, setup):

        page = SAEnquiryListPage(setup)
        page.goto_page()

        page.search("     ")

        assert page.is_row_present()

