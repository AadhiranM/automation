import pytest

from pages.superadmin.Manufacturer.sa_manufacturer_list_page import (
    SAManufacturerListPage
)

from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage
)

from pages.superadmin.QRManagement.sa_category_create_page import (
    SACategoryCreatePage
)


@pytest.mark.superadmin
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestCategoryCreateNegative:

    def test_blank_manufacturer_name(
            self,
            setup,
            category_name
    ):

        list_page = SACategoryListPage(setup)

        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)

        create_page.wait_for_modal()

        create_page.enter_category_name(
            category_name
        )

        create_page.click_save()

        assert create_page.is_error_present(
            "Please select a manufacturer."
        )

    def test_blank_category_name(
            self,
            setup
    ):

        manufacturer_page = SAManufacturerListPage(setup)

        manufacturer_page.goto_page()

        manufacturer_email = (
            manufacturer_page.get_first_approved_manufacturer()
        )

        list_page = SACategoryListPage(setup)

        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)

        create_page.wait_for_modal()

        create_page.select_manufacturer(
            manufacturer_email
        )

        create_page.click_save()

        assert create_page.is_error_present(
            "The category is required."
        )

    def test_invalid_category_name(
            self,
            setup
    ):

        manufacturer_page = SAManufacturerListPage(setup)

        manufacturer_page.goto_page()

        manufacturer_email = (
            manufacturer_page.get_first_approved_manufacturer()
        )

        list_page = SACategoryListPage(setup)

        list_page.goto_page()

        list_page.click_create()

        create_page = SACategoryCreatePage(setup)

        create_page.wait_for_modal()

        create_page.select_manufacturer(
            manufacturer_email
        )

        create_page.enter_category_name(
            "123456"
        )

        create_page.click_save()

        assert create_page.is_error_present(
            "The category should contain only letters and spaces."
        )

    # ============================================================
    # DUPLICATE CATEGORY NAME
    # Existing Category + Same Manufacturer
    # ============================================================
    def test_duplicate_category_name_for_same_manufacturer(
            self,
            setup
    ):

        list_page = SACategoryListPage(setup)

        # --------------------------------------------------------
        # STEP 1: Open Category List
        # --------------------------------------------------------
        list_page.goto_page()

        # --------------------------------------------------------
        # STEP 2: Get existing category and manufacturer
        # from the SAME first row
        # --------------------------------------------------------
        existing_category = (
            list_page.get_first_category_name()
        )

        existing_manufacturer = (
            list_page.get_first_manufacturer_name()
        )

        print(
            f"Existing Category     : {existing_category}"
        )

        print(
            f"Existing Manufacturer  : {existing_manufacturer}"
        )

        assert existing_category, \
            "Existing category name was not found"

        assert existing_manufacturer, \
            "Existing manufacturer was not found"

        # --------------------------------------------------------
        # STEP 3: Open Create Category modal
        # --------------------------------------------------------
        list_page.click_create()

        create_page = SACategoryCreatePage(setup)

        create_page.wait_for_modal()

        # --------------------------------------------------------
        # STEP 4: Select SAME manufacturer
        # --------------------------------------------------------
        create_page.select_manufacturer(
            existing_manufacturer
        )

        # --------------------------------------------------------
        # STEP 5: Enter SAME category name
        # --------------------------------------------------------
        create_page.enter_category_name(
            existing_category
        )

        # --------------------------------------------------------
        # STEP 6: Click Save
        # --------------------------------------------------------
        create_page.click_save()

        # --------------------------------------------------------
        # STEP 7: Validate duplicate category error
        # --------------------------------------------------------
        assert create_page.is_error_present(
            "This category already exists."
        ), \
            "Duplicate category validation message was not displayed"

        print(
            "Duplicate category validation passed"
        )