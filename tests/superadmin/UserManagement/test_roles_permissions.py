import time
import pytest

from pages.superadmin.UserManagement.sa_roles_permissions_page import SARolesPermissionsPage

from utilities.data_generator import generate_user_name


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCreateRole:
    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_create_role(self, setup):
        page = SARolesPermissionsPage(setup)

        role_name = f"{generate_user_name()} Role"

        page.goto_page()

        page.create_role(
            role_name=role_name,
            status="Active"
        )

        time.sleep(5)

        # page.driver.get(
        #     "https://beta.digitathya.com/admin/role?reset_filters=1"
        # )
        #
        # first_role = page.get_first_row_role_name()
        #
        # assert role_name == first_role
        page.goto_list_page()

        page.search_role(role_name)

        first_role = page.get_first_row_role_name()

        assert role_name == first_role