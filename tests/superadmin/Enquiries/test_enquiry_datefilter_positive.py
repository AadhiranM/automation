import pytest
from datetime import date, timedelta

from pages.superadmin.Enquiries.sa_enquiry_list_page import SAEnquiryListPage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestEnquiryDateFilterPositive:

    def test_today_date_filter(self, setup):
        page = SAEnquiryListPage(setup)
        today = date.today()

        page.filter_inline_created_at(today, today)

        dates = page.get_all_created_dates()

        assert all(d == today for d in dates), "❌ Non-today entries returned!"

    def test_yesterday_date_filter(self, setup):
        page = SAEnquiryListPage(setup)
        yesterday = date.today() - timedelta(days=1)

        page.filter_inline_created_at(yesterday, yesterday)

        dates = page.get_all_created_dates()

        assert all(d == yesterday for d in dates), "❌ Entries outside yesterday returned!"

    def test_date_range_last_7_days(self, setup):
        page = SAEnquiryListPage(setup)
        end = date.today()
        start = end - timedelta(days=7)

        page.filter_inline_created_at(start, end)

        dates = page.get_all_created_dates()

        assert all(start <= d <= end for d in dates), "❌ Entries outside 7-day range returned!"

    def test_date_status_combination(self, setup):
        """
        Example:
        "New" status + last 3 days filter
        """
        page = SAEnquiryListPage(setup)

        start = date.today() - timedelta(days=3)
        end = date.today()

        page.filter_with_date_status_search(start, end, status="New")

        # Validate date
        dates = page.get_all_created_dates()
        assert all(start <= d <= end for d in dates), "❌ Wrong dates!"

        # Validate status
        assert page.table_contains_status("New")

    def test_date_search_status_combination(self, setup):
        page = SAEnquiryListPage(setup)

        start = date.today() - timedelta(days=5)
        end = date.today()

        page.filter_with_date_status_search(
            start, end,
            status="New",
            query="test"
        )

        dates = page.get_all_created_dates()
        assert all(start <= d <= end for d in dates)

        assert page.table_contains_status("New")
        assert page.table_contains_text("test")
