import pytest

from pages.superadmin.UserManagement.sa_user_list_page import (
    SAUserListPage
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestUserList:

    # =====================================================
    # SEARCH
    # =====================================================

    def test_search_user(self, setup):

        page = SAUserListPage(setup)

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
    def test_filter_by_status(
            self,
            setup,
            status
    ):

        page = SAUserListPage(setup)

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

        page = SAUserListPage(setup)

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

        page = SAUserListPage(setup)

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

        page = SAUserListPage(setup)

        page.goto_page()

        page.go_to_page(2)

        assert (
                page.is_row_present()
                or
                page.has_no_data()
        )