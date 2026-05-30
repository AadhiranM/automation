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

        # VIEW

        page.click_view()

        assert "show" in setup.current_url.lower()

        setup.back()

        time.sleep(3)

        # EDIT USER

        page.click_edit()

        updated_name = generate_user_name()

        page.update_user_name(updated_name)

        time.sleep(4)

        # VALIDATE UPDATED NAME

        first_row_name = page.get_first_row_name()

        assert updated_name == first_row_name

        # ROLE & PERMISSIONS

        page.click_role_permissions()

        assert "permission" in setup.current_url.lower()

        setup.back()

        time.sleep(3)

        # STATUS VALIDATION

        current_status = page.get_first_row_status()

        if current_status == "Active":

            page.click_three_dots()

            page.click_suspend()

            page.confirm_suspend()

            updated_status = page.get_first_row_status()

            assert updated_status == "Suspended"

        else:

            page.click_three_dots()

            page.confirm_activate()

            page.confirm_activate()

            updated_status = page.get_first_row_status()

            assert updated_status == "Active"