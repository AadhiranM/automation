import time
import pytest

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

    def test_create_user(self, setup):

        # ------------------------------------
        # Get Manufacturer from Roles page
        # ------------------------------------

        role_page = SARolesPermissionsPage(setup)

        role_page.goto_list_page()

        manufacturer = role_page.get_first_manufacturer()

        users_before = role_page.get_first_users_count()

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
            mobile=generate_mobile_number(),
            password=generate_password(),
            status="Active"
        )

        time.sleep(5)

        # ------------------------------------
        # Verify User created
        # ------------------------------------

        list_page = SAUserListPage(setup)

        list_page.goto_page()

        first_row_name = list_page.get_first_row_name()

        assert user_name == first_row_name

        # ------------------------------------
        # Verify Users count increased
        # ------------------------------------

        # ------------------------------------
        # Verify Users count increased
        # ------------------------------------

        role_page.goto_list_page()

        # wait for page refresh
        time.sleep(2)

        users_after = role_page.get_first_users_count()

        print(f"Users Before : {users_before}")
        print(f"Users After  : {users_after}")

        if users_before == "-":
            assert users_after == "1 users"
        else:
            before = int(users_before.split()[0])
            after = int(users_after.split()[0])

            assert after == before + 1