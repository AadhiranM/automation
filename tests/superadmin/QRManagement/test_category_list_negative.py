import pytest
from datetime import date, timedelta

from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryListNegative:

    # ============================================================
    # 1. SEARCH WITH INVALID / NON-EXISTING CATEGORY NAME
    # ============================================================
    def test_search_invalid_category_name(self, setup):

        page = SACategoryListPage(setup)

        # Open Category List
        page.goto_page()

        # Intentionally use a category name which should not exist
        invalid_category = "InvalidCategory_999999999"

        print(
            f"Searching invalid category: {invalid_category}"
        )

        page.search(invalid_category)

        # Validate No Result Found
        assert page.has_no_data_message(), \
            "No Result Found message was not displayed"

        assert "Sorry! No Result Found" in page.get_no_data_message(), \
            f"Unexpected message: {page.get_no_data_message()}"

        print(
            "Invalid category search validation passed"
        )

    # ============================================================
    # 2. FILTER WITH OLD / NON-EXISTING DATE RANGE
    # ============================================================
    def test_filter_invalid_created_date_range(self, setup):

        page = SACategoryListPage(setup)

        # Open Category List
        page.goto_page()

        # Use an old date range where category records
        # should not exist.
        #
        # Current date - 15 months
        # This keeps the range within Flatpickr's current
        # navigation capability.
        end = date.today() - timedelta(days=450)
        start = end - timedelta(days=7)

        print(f"Invalid Date Start : {start}")
        print(f"Invalid Date End   : {end}")

        page.filter_inline_created_at(
            start,
            end
        )

        # Validate No Result Found
        assert page.has_no_data_message(), \
            "No Result Found message was not displayed for invalid date range"

        assert "Sorry! No Result Found" in page.get_no_data_message(), \
            f"Unexpected message: {page.get_no_data_message()}"

        print(
            "Invalid created-date filter validation passed"
        )