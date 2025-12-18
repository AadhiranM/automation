import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_view_page import SAManufacturerViewPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerViewPositive:

    def test_view_manufacturer_details(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.search("frankfurt")
        page.open_action_menu()
        page.click_view()

        view = SAManufacturerViewPage(setup)
        assert view.is_visible(view.COMPANY_NAME)
        assert view.is_visible(view.EMAIL)
        assert view.is_visible(view.STATUS)
