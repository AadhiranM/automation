import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerListNegative:

    @pytest.mark.sanity
    def test_search_by_invalid_company_name(self, setup):
        page = SAManufacturerListPage(setup)

        page.goto_page()

        page.search("pwoo")

        assert page.has_no_data_message()

    @pytest.mark.sanity
    def test_search_by_invalid_pan_number(self, setup):
        page = SAManufacturerListPage(setup)

        page.goto_page()

        page.search("ABCDE1234h")

        assert page.has_no_data_message()

    @pytest.mark.sanity
    def test_search_by_invalid_business_email(self, setup):
        page = SAManufacturerListPage(setup)

        page.goto_page()

        page.search("ruchiii@mailinatorr.com")

        assert page.has_no_data_message()

    def test_search_with_empty_value_returns_all_results(self, setup):
        page = SAManufacturerListPage(setup)

        page.goto_page()

        page.search("")

        assert page.is_row_present()

    def test_search_with_special_characters(self, setup):
        page = SAManufacturerListPage(setup)

        page.goto_page()

        page.search("@@@###!!!")

        assert page.has_no_data_message()