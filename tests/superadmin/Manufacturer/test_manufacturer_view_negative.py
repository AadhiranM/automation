import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerViewNegative:

    def test_view_without_selection(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()

        # No action clicked → ensure page still stable
        assert page.is_row_present()
