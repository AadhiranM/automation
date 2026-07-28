import pytest
from datetime import date, timedelta
from pages.superadmin.QRManagement.sa_category_list_page import SACategoryListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryListPositive:

    def test_search_category(self, setup):
        page = SACategoryListPage(setup)

        page.goto_page()

        category = page.get_first_category_name()

        page.search(category)

        assert page.get_first_category_name() == category

    def test_search_manufacturer(self, setup):
        page = SACategoryListPage(setup)

        page.goto_page()

        manufacturer = page.get_first_manufacturer_name()

        page.search(manufacturer)

        assert page.get_first_manufacturer_name() == manufacturer
    def test_filter_status_active(self, setup):
        page = SACategoryListPage(setup)
        page.goto_page()
        page.filter_by_status("Active")
        assert page.is_row_present()

    def test_entries_per_page_25(self, setup):
        page = SACategoryListPage(setup)
        page.goto_page()
        page.set_entries_per_page(25)
        assert page.is_row_present()

    def test_pagination(self, setup):
        page = SACategoryListPage(setup)
        page.goto_page()
        page.click_next()
        assert page.is_row_present()
        page.click_previous()
        assert page.is_row_present()

    def test_filter_created_date_range(self, setup):
        page = SACategoryListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_inline_created_at(start, end)
        rows = page.get_all_created_dates()



        print("Start:", start)
        print("End  :", end)
        print("Rows :", rows)

        if not rows:
            pytest.skip("No categories in selected range")

        for r in rows:
            print("Checking:", r)
            assert start <= r <= end