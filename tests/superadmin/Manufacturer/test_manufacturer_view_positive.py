import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_view_page import SAManufacturerViewPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerViewPositive:

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_view_manufacturer_details(self, setup):

        page = SAManufacturerListPage(setup)

        page.goto_page()

        # Get dynamic first row details
        company = page.get_first_row_company()
        email = page.get_first_row_email()

        # Search dynamically
        page.search(company)

        # Open View page
        page.open_action_menu()
        page.click_view()

        view = SAManufacturerViewPage(setup)

        # Verify URL
        assert "show" in setup.current_url.lower()

