import time
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.superadmin.UserManagement.sa_user_create_page import SAUserCreatePage
from pages.superadmin.UserManagement.sa_user_list_page import SAUserListPage
from pages.superadmin.UserManagement.sa_roles_permissions_page import (
    SARolesPermissionsPage
)

from utilities.data_generator import (
    generate_user_name,
    generate_user_email,
    generate_mobile_number,
    generate_password
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestCreateUser:
    @pytest.mark.smoke
    @pytest.mark.sanity
    def test_create_user(self, setup):

        # ------------------------------------
        # Get Role details
        # ------------------------------------

        role_page = SARolesPermissionsPage(setup)

        role_page.goto_list_page()

        role_name = role_page.get_first_row_role_name()

        role_page.search_role(role_name)

        manufacturer = role_page.get_first_manufacturer()

        users_before = role_page.get_first_users_count()

        print(f"Users Before : {users_before}")

        # ------------------------------------
        # Create User
        # ------------------------------------

        create_page = SAUserCreatePage(setup)

        user_name = generate_user_name()

        create_page.goto_page()

        create_page.create_user(
            name=user_name,
            email=generate_user_email(),
            manufacturer=manufacturer,
            role=role_name,
            mobile=generate_mobile_number(),
            password=generate_password(),
            status="Active"
        )

        # ------------------------------------
        # Verify User created
        # ------------------------------------

        list_page = SAUserListPage(setup)

        list_page.goto_page()

        list_page.search_user(user_name)

        assert list_page.get_first_row_name() == user_name

        # # ------------------------------------
        # # Verify Users count increased
        # # ------------------------------------
        #
        # # ------------------------------------
        # # Verify Users count increased
        # # ------------------------------------
        #
        # role_page.goto_list_page()
        #
        # role_page.search_role(role_name)
        #
        # # Wait until the Users count is updated
        # WebDriverWait(setup, 30).until(
        #     lambda d: role_page.get_first_users_count() != users_before
        # )
        #
        # users_after = role_page.get_first_users_count()
        #
        # print(f"Users Before : {users_before}")
        # print(f"Users After  : {users_after}")
        #
        # if users_before == "-":
        #     assert users_after == "1 users"
        # else:
        #     before = int(users_before.split()[0])
        #     after = int(users_after.split()[0])
        #
        #     assert after == before + 1