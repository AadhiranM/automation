import pytest
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import SAManufacturerListPage
from pages.superadmin.Manufacturer.sa_manufacturer_create_page import SAManufacturerCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerCreateNegative:

    def open_create_modal(self, setup):
        list_page = SAManufacturerListPage(setup)
        list_page.goto_page()
        list_page.click_create()

        create_page = SAManufacturerCreatePage(setup)
        create_page.wait_for_page()

        # 🔑 Disable browser validation ONLY for negative tests
        create_page.disable_browser_validation()

        return create_page

    # ---------------- EMPTY FIELDS ----------------
    def test_create_manufacturer_with_empty_fields(self, setup):
        create_page = self.open_create_modal(setup)

        create_page.click_save()

        assert create_page.is_email_error_visible()
        assert create_page.is_company_error_visible()

    # ---------------- INVALID EMAIL ----------------
    def test_create_manufacturer_with_invalid_email_format(self, setup):
        create_page = self.open_create_modal(setup)

        create_page.fill_email("invalid")
        create_page.fill_company_name("Sydney Tea Shop")
        create_page.click_save()

        assert create_page.is_email_error_visible()

    # ---------------- SHORT COMPANY NAME ----------------
    def test_create_manufacturer_with_short_company_name(self, setup):
        create_page = self.open_create_modal(setup)

        create_page.fill_email("short@mailinator.com")
        create_page.fill_company_name("T")
        create_page.click_save()

        assert create_page.is_company_error_visible()

    # ---------------- DUPLICATE EMAIL ----------------
    def test_create_manufacturer_with_existing_email(self, setup):
        create_page = self.open_create_modal(setup)

        create_page.fill_email("Sydney@mailinator.com")
        create_page.fill_company_name("Unique Company Name")
        create_page.click_save()

        assert create_page.is_email_error_visible()

    # ---------------- DUPLICATE COMPANY ----------------
    def test_create_manufacturer_with_existing_company_name(self, setup):
        create_page = self.open_create_modal(setup)

        create_page.fill_email("unique@mailinator.com")
        create_page.fill_company_name("Sydney Tea Shop")
        create_page.click_save()

        assert create_page.is_company_error_visible()

    # ---------------- DUPLICATE EMAIL + COMPANY ----------------
    def test_create_manufacturer_with_existing_email_and_company(self, setup):
        create_page = self.open_create_modal(setup)

        create_page.fill_email("Sydney@mailinator.com")
        create_page.fill_company_name("Sydney Tea Shop")
        create_page.click_save()

        assert create_page.is_email_error_visible()
        assert create_page.is_company_error_visible()
