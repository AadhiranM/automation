import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_filter_page import SAManufacturerFilterPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerFiltersNegative:

    def test_apply_disabled_without_any_input(self, setup):
        SAManufacturerListPage(setup).goto_page()
        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        assert not filter_page.is_apply_enabled()

    def test_filter_invalid_company_name(self, setup):
        SAManufacturerListPage(setup).goto_page()
        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        filter_page.set_company_name("Teaa")
        filter_page.click_apply()

        assert filter_page.is_no_data_displayed()

    def test_filter_invalid_business_email(self, setup):
        SAManufacturerListPage(setup).goto_page()
        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        filter_page.set_business_email("smarvell@mailinator.com")
        filter_page.click_apply()

        assert filter_page.is_no_data_displayed()

    def test_filter_invalid_pan_number(self, setup):
        SAManufacturerListPage(setup).goto_page()
        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        filter_page.set_pan_number("AAYCA8957B")
        filter_page.click_apply()

        assert filter_page.is_no_data_displayed()

    def test_filter_multiple_invalid_inputs(self, setup):
        SAManufacturerListPage(setup).goto_page()
        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        filter_page.set_company_name("testingda")
        filter_page.set_business_email("smarvel@mailinator.com")
        filter_page.set_pan_number("ABCDE1234F")
        filter_page.click_apply()

        assert filter_page.is_no_data_displayed()
