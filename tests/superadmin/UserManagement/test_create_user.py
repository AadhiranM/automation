import time
import pytest

from pages.superadmin.UserManagement.sa_user_create_page import SAUserCreatePage
from pages.superadmin.UserManagement.sa_user_list_page import SAUserListPage

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

        create_page = SAUserCreatePage(setup)

        user_name = generate_user_name()

        create_page.goto_page()

        create_page.create_user(
            name=user_name,
            email=generate_user_email(),
            mobile=generate_mobile_number(),
            password=generate_password(),
            status="Active"
        )

        time.sleep(5)

        list_page = SAUserListPage(setup)

        list_page.goto_page()

        first_row_name = list_page.get_first_row_name()

        assert user_name == first_row_name