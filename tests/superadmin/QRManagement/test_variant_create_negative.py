import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.superadmin.QRManagement.sa_variant_list_page import (
    SAVariantListPage
)

from pages.superadmin.QRManagement.sa_variant_create_page import (
    SAVariantCreatePage
)

from pages.superadmin.QRManagement.sa_category_list_page import (
    SACategoryListPage
)

from utilities.data_generator import (
    generate_variant_value
)


@pytest.mark.superadmin
@pytest.mark.negative
@pytest.mark.sanity
@pytest.mark.usefixtures("login_superadmin")
class TestVariantCreateNegative:

    # ============================================================
    # TOAST
    # ============================================================

    TOAST_MESSAGE = (
        By.XPATH,
        "//div[contains(@class,'toastify') "
        "and not(contains(@style,'display: none'))]"
    )

    def get_visible_toast_message(self, driver):

        toast = WebDriverWait(
            driver,
            10
        ).until(
            EC.visibility_of_element_located(
                self.TOAST_MESSAGE
            )
        )

        message = toast.text.strip()

        print(
            f"Toast Message : {message}"
        )

        return message

    # ============================================================
    # GET EXISTING VARIANT DATA
    # Manufacturer + Category + Variant Type
    # from the SAME row
    # ============================================================

    def get_existing_variant_data(self, driver):

        list_page = SAVariantListPage(driver)

        list_page.goto_page()
        list_page.wait_for_table()

        rows = driver.find_elements(
            *list_page.TABLE_ROWS
        )

        for row in rows:

            cells = row.find_elements(
                By.TAG_NAME,
                "td"
            )

            if len(cells) < 3:
                continue

            manufacturer = cells[0].text.strip()
            category = cells[1].text.strip()
            variant_type = cells[2].text.strip()

            if (
                manufacturer
                and category
                and variant_type
                and "No Variants" not in variant_type
            ):

                print(
                    f"Existing Manufacturer : {manufacturer}"
                )

                print(
                    f"Existing Category     : {category}"
                )

                print(
                    f"Existing Variant Type : {variant_type}"
                )

                return (
                    manufacturer,
                    category,
                    variant_type
                )

        raise Exception(
            "No existing variant found in Variant List"
        )

    # ============================================================
    # OPEN CREATE VARIANT PAGE
    # ============================================================

    def open_create_page(
            self,
            driver,
            manufacturer,
            category
    ):

        list_page = SAVariantListPage(driver)

        list_page.goto_page()
        list_page.click_create()

        create_page = SAVariantCreatePage(driver)

        create_page.wait_for_page()

        create_page.select_manufacturer(
            manufacturer
        )

        create_page.select_category(
            category
        )

        return create_page

    # ============================================================
    # 1. DUPLICATE VARIANT TYPE
    #
    # Existing Variant Type
    # New Variant Value
    #
    # Expected:
    # Product variant type(s) already exist: <type>
    # ============================================================

    def test_create_duplicate_variant_type(
            self,
            setup
    ):

        (
            manufacturer,
            category,
            existing_variant_type
        ) = self.get_existing_variant_data(
            setup
        )

        create_page = self.open_create_page(
            setup,
            manufacturer,
            category
        )

        # Existing Variant Type
        create_page.enter_variant_type(
            existing_variant_type
        )

        # New Variant Value
        create_page.enter_variant_value(
            generate_variant_value()
        )

        # Save
        create_page.click_save()

        # IMPORTANT:
        # Capture Toast immediately using visibility
        toast_message = self.get_visible_toast_message(
            setup
        )

        assert (
            "Product variant type(s) already exist"
            in toast_message
        ), (
            f"Unexpected duplicate variant toast: "
            f"{toast_message}"
        )

        assert (
            existing_variant_type.lower()
            in toast_message.lower()
        ), (
            f"Existing variant type "
            f"'{existing_variant_type}' "
            f"was not mentioned in toast: "
            f"{toast_message}"
        )

        print(
            "Duplicate variant type validation passed"
        )

    # ============================================================
    # 2. VARIANT TYPE FILLED
    #    VARIANT VALUE MISSING
    #
    # Expected:
    # Please fill all added Variant Type and
    # Variant Value fields.
    # ============================================================

    def test_create_variant_missing_variant_value(
            self,
            setup
    ):

        category_page = SACategoryListPage(
            setup
        )

        category_page.goto_page()

        manufacturer, category = (
            category_page
            .get_first_active_category_and_manufacturer()
        )

        create_page = self.open_create_page(
            setup,
            manufacturer,
            category
        )

        # Fill Variant Type
        create_page.enter_variant_type(
            "TestVariantType"
        )

        # Variant Value intentionally NOT filled

        # Save
        create_page.click_save()

        # Capture Toast immediately
        toast_message = self.get_visible_toast_message(
            setup
        )

        expected_message = (
            "Please fill all added Variant Type "
            "and Variant Value fields."
        )

        assert expected_message in toast_message, (
            f"Unexpected validation toast: "
            f"{toast_message}"
        )

        print(
            "Missing variant value validation passed"
        )

    # ============================================================
    # 3. VARIANT TYPE MISSING
    #    VARIANT VALUE FILLED
    #
    # Expected:
    # Please fill all added Variant Type and
    # Variant Value fields.
    # ============================================================

    def test_create_variant_missing_variant_type(
            self,
            setup
    ):

        category_page = SACategoryListPage(
            setup
        )

        category_page.goto_page()

        manufacturer, category = (
            category_page
            .get_first_active_category_and_manufacturer()
        )

        create_page = self.open_create_page(
            setup,
            manufacturer,
            category
        )

        # Variant Type intentionally NOT filled

        # Fill Variant Value
        create_page.enter_variant_value(
            generate_variant_value()
        )

        # Save
        create_page.click_save()

        # Capture Toast immediately
        toast_message = self.get_visible_toast_message(
            setup
        )

        expected_message = (
            "Please fill all added Variant Type "
            "and Variant Value fields."
        )

        assert expected_message in toast_message, (
            f"Unexpected validation toast: "
            f"{toast_message}"
        )

        print(
            "Missing variant type validation passed"
        )