import pytest
from datetime import date, timedelta
from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerListPositive:

    def test_search_by_company_name(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.search("test")
        assert page.is_row_present()

    def test_search_by_email(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.search("mailinator")
        assert page.is_row_present()

    def test_filter_status_pending(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.filter_by_status("Pending")
        assert page.is_row_present()

    def test_entries_per_page_25(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.set_entries_per_page("25")
        assert page.is_row_present()

    def test_pagination_next_previous(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.click_next()
        assert page.is_row_present()
        page.click_previous()
        assert page.is_row_present()

    def test_go_to_specific_page(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()
        page.go_to_page("2")
        assert page.is_row_present()

    def test_filter_created_date_range(self, setup):
        page = SAManufacturerListPage(setup)
        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_inline_created_at(start, end)
        rows = page.get_all_created_dates()

        assert len(rows) > 0
        for r in rows:
            assert start <= r <= end
