import time
import pytest
from datetime import date, timedelta
from pages.superadmin.Applicationusers.sa_application_user_page import (
    SAApplicationUserPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestApplicationUsers:

    @pytest.mark.sanity
    def test_search_user(self, setup):
        page = SAApplicationUserPage(setup)

        page.goto_page()

        user_name = page.search_first_user()

        assert user_name != ""

    # =====================================================
    # STATUS FILTER
    # =====================================================

    @pytest.mark.parametrize(
        "status",
        [
            "Active",
            "Suspended"
        ]
    )
    @pytest.mark.sanity
    def test_filter_by_status(
            self,
            setup,
            status
    ):
        page = SAApplicationUserPage(setup)

        page.goto_page()

        page.filter_by_status(status)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # =====================================================
    # ENTRIES
    # =====================================================

    @pytest.mark.parametrize(
        "count",
        [
            "10",
            "25",
            "50"
        ]
    )
    def test_entries_per_page(
            self,
            setup,
            count
    ):
        page = SAApplicationUserPage(setup)

        page.goto_page()

        page.set_entries_per_page(count)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    # =====================================================
    # PAGINATION
    # =====================================================

    def test_next_previous_page(self, setup):
        page = SAApplicationUserPage(setup)

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
        page = SAApplicationUserPage(setup)

        page.goto_page()

        page.go_to_page(2)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    def test_filter_date_range(self, setup):
        page = SAApplicationUserPage(setup)

        page.goto_page()

        start = date.today() - timedelta(days=7)
        end = date.today()

        page.filter_by_date(start, end)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_view_user(self, setup):
        page = SAApplicationUserPage(setup)

        page.goto_page()

        page.click_view()

        assert (
                "show" in setup.current_url.lower()
                or
                "view" in setup.current_url.lower()
        )

    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_user_status_toggle(self, setup):

        page = SAApplicationUserPage(setup)

        page.goto_page()

        current_status = page.get_first_row_status()

        if current_status == "Active":

            page.suspend_user()

            time.sleep(3)

            setup.refresh()

            assert page.get_first_row_status() == "Suspended"

        else:

            page.activate_user()

            time.sleep(3)

            setup.refresh()

            assert page.get_first_row_status() == "Active"