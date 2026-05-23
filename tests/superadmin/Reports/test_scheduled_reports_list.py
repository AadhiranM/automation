import pytest
from datetime import date, timedelta
from pages.superadmin.Reports.sa_scheduled_reports_list_page import SAScheduledReportsPage



@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestScheduledReports:

    # ==========================
    # SEARCH
    # ==========================
    def test_search(self, setup):
        page = SAScheduledReportsPage(setup)

        page.goto_page()

        value = page.search_first_record()

        assert value != ""

    # ==========================
    # STATUS FILTER
    # ==========================
    @pytest.mark.parametrize(
        "status",
        [
            "All",
            "Active",
            "Inactive"
        ]
    )
    def test_filter_status(self, setup, status):
        page = SAScheduledReportsPage(setup)

        page.goto_page()

        page.filter_by_status(status)

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================
    # DATE FILTER
    # ==========================
    def test_filter_date_range(self, setup):
        page = SAScheduledReportsPage(setup)

        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_date(start, end)

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================
    # ENTRIES
    # ==========================
    @pytest.mark.parametrize(
        "count",
        [
            "10",
            "25",
            "50",
            "100"
        ]
    )
    def test_entries_per_page(self, setup, count):
        page = SAScheduledReportsPage(setup)

        page.goto_page()

        page.set_entries_per_page(count)

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    # ==========================
    # PAGINATION
    # ==========================
    def test_next_previous_page(self, setup):
        page = SAScheduledReportsPage(setup)

        page.goto_page()

        page.click_next()

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

        page.click_previous()

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )

    def test_go_to_page_2(self, setup):
        page = SAScheduledReportsPage(setup)

        page.goto_page()

        page.go_to_page("2")

        assert (
            page.is_row_present()
            or
            page.has_no_data()
        )