import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_filter_page import SAManufacturerFilterPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerFilters:

    # ---------------- BASIC STATE ----------------
    def test_filter_initial_state(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()

        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        assert not filter_page.is_apply_enabled(), "Apply should be disabled initially"
        assert not filter_page.is_clear_enabled(), "Clear should be disabled initially"

    # ---------------- POSITIVE ----------------
    def test_filter_by_company_name(self, setup):
        SAManufacturerListPage(setup).goto_page()

        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()
        filter_page.set_company_name("test")

        assert filter_page.is_apply_enabled()
        filter_page.click_apply()
        assert filter_page.is_row_present()

    def test_filter_by_business_email(self, setup):
        SAManufacturerListPage(setup).goto_page()

        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()
        filter_page.set_business_email("mailinator.com")

        filter_page.click_apply()
        assert filter_page.is_row_present()

    def test_filter_by_pan_number(self, setup):
        SAManufacturerListPage(setup).goto_page()

        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()
        filter_page.set_pan_number("ABCDE1234F")

        filter_page.click_apply()
        assert filter_page.is_row_present()

    def test_filter_by_approval_status(self, setup):
        SAManufacturerListPage(setup).goto_page()

        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()
        filter_page.select_approval_status("Pending")

        filter_page.click_apply()
        assert filter_page.is_row_present()

    def test_filter_by_clear_filter(self, setup):
        # Navigate to Manufacturer list
        SAManufacturerListPage(setup).goto_page()

        filter_page = SAManufacturerFilterPage(setup)
        filter_page.open_filter_drawer()

        # Enter ALL filter inputs
        filter_page.set_company_name("Teaa")
        filter_page.set_business_email("Tea@mailinator.com")
        filter_page.set_pan_number("AAYCA8957B")
        filter_page.select_approval_status("Pending")

        # Validate Apply is enabled
        assert filter_page.is_apply_enabled(), \
            "Apply should be enabled after entering filter values"

        # Click Clear Filter
        filter_page.click_clear()

        # ---------------- ASSERTIONS AFTER CLEAR ----------------

        # Apply button should be disabled
        assert not filter_page.is_apply_enabled(), \
            "Apply should be disabled after clearing filters"

        # Clear button should be disabled
        assert not filter_page.is_clear_enabled(), \
            "Clear Filter should be disabled after clearing filters"

        # All fields should be empty
        assert filter_page.is_company_name_empty(), \
            "Company name field should be cleared"

        assert filter_page.is_business_email_empty(), \
            "Business email field should be cleared"

        assert filter_page.is_pan_number_empty(), \
            "PAN number field should be cleared"

        assert filter_page.is_approval_status_default(), \
            "Approval status should reset to default"

        # List should be reset (rows visible)
        assert filter_page.is_row_present(), \
            "Manufacturer list should be reset after clearing filters"


