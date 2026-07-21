import time
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.superadmin.UserManagement.sa_user_list_page import SAUserListPage
from utilities.data_generator import (
    generate_user_name,
    generate_mobile_number
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestUserActions:

    def test_user_actions(self, setup):

        page = SAUserListPage(setup)

        page.goto_page()

        # =====================================================
        # VIEW USER
        # =====================================================

        page.click_view()

        assert "show" in setup.current_url.lower()

        setup.back()

        time.sleep(3)

        # =====================================================
        # EDIT USER
        # =====================================================

        page.click_edit()

        updated_name = generate_user_name()
        updated_mobile = generate_mobile_number()

        page.update_user_details(
            updated_name,
            updated_mobile
        )

        # Verify update redirects back to User List page
        WebDriverWait(setup, 20).until(
            lambda d: "/admin/user" in d.current_url.lower()
        )

        assert "/admin/user" in setup.current_url.lower()

        # =====================================================
        # ROLE & PERMISSIONS
        # =====================================================

        # Search result is still filtered to updated user,
        # so action is performed on the correct user
        # =========================
        # ROLE & PERMISSIONS
        # =========================

        # Ensure we are back on a fully loaded User List page
        page.goto_page()
        page.wait_for_results()

        page.click_role_permissions()

        assert "permission" in setup.current_url.lower()

        setup.back()

        time.sleep(3)

        page.goto_page()

        # =====================================================
        # STATUS CHANGE
        # =====================================================

        # Search the SAME updated user again
        # This prevents parallel tests from changing
        # which user appears in the first row
        page.search_user(updated_name)

        current_status = page.get_first_row_status()

        print(f"BEFORE STATUS = {current_status}")

        if current_status == "Active":

            page.suspend_user()

            time.sleep(3)

            setup.refresh()

            page.wait_for_results()

            updated_status = page.get_first_row_status()

            print(f"AFTER STATUS = {updated_status}")

            assert updated_status == "Suspended"

        else:

            page.activate_user()

            time.sleep(3)

            setup.refresh()

            page.wait_for_results()

            updated_status = page.get_first_row_status()

            print(f"AFTER STATUS = {updated_status}")

            assert updated_status == "Active"