import time
import pytest

from pages.superadmin.UserManagement.sa_user_list_page import SAUserListPage
from utilities.data_generator import generate_user_name


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestUserActions:

    def test_user_actions(self, setup):

        page = SAUserListPage(setup)

        page.goto_page()

        # =========================
        # VIEW USER
        # =========================

        page.click_view()

        assert "show" in setup.current_url.lower()

        setup.back()

        time.sleep(3)

        # =========================
        # EDIT USER
        # =========================

        page.click_edit()

        updated_name = generate_user_name()

        page.update_user_name(updated_name)

        time.sleep(3)

        page.goto_page()

        first_row_name = page.get_first_row_name()

        assert updated_name == first_row_name

        # =========================
        # ROLE & PERMISSIONS
        # =========================

        page.click_role_permissions()

        assert "permission" in setup.current_url.lower()

        setup.back()

        time.sleep(3)

        page.goto_page()

        # =========================
        # STATUS CHANGE
        # =========================

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