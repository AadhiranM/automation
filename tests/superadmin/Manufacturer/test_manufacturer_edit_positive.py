import pytest

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.Manufacturer.sa_manufacturer_edit_page import (
    SAManufacturerEditPage
)

from utilities.data_generator import (
    generate_manufacturer_name,
    generate_mailinator_email
)


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestManufacturerEditPositive:

    def test_edit_pending_manufacturer_and_verify_update(
            self,
            setup
    ):

        list_page = SAManufacturerListPage(setup)

        list_page.goto_page()

        # Open first row -> Edit
        list_page.open_action_menu()

        list_page.click_edit()

        edit_page = SAManufacturerEditPage(setup)

        edit_page.wait_for_page()

        # Dynamic values for CI/CD
        new_email = generate_mailinator_email()

        new_company = generate_manufacturer_name()

        # Update values
        edit_page.update_email(
            new_email
        )

        edit_page.update_company_name(
            new_company
        )

        edit_page.click_update()

        edit_page.wait_for_modal_close()

        list_page.search_company(
            new_company
        )

        list_page.wait_for_results()

        first_row = (
            list_page.get_first_row_company_name()
        )

        assert (
                new_company in first_row
        ), f"Company not updated: {new_company}"