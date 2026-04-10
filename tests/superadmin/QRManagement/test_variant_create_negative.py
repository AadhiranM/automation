import time

import pytest
from pages.superadmin.QRManagement.sa_variant_list_page import SAVariantListPage
from pages.superadmin.QRManagement.sa_variant_create_page import SAVariantCreatePage


@pytest.mark.superadmin
@pytest.mark.usefixtures("login_superadmin")
class TestVariantCreateNegative:

    # =========================================================
    # COMMON METHOD
    # =========================================================
    def open_create_page(self, driver):
        list_page = SAVariantListPage(driver)
        list_page.goto_page()
        list_page.click_create()

        create_page = SAVariantCreatePage(driver)
        create_page.wait_for_page()

        return create_page


    # =========================================================
    # 1. SAVE BUTTON DISABLED INITIALLY
    # =========================================================
    def test_save_button_disabled_initially(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        assert create_page.is_save_button_disabled()


    # =========================================================
    # 2. SAVE BUTTON ENABLED WHEN VARIANT TYPE ENTERED
    # =========================================================
    def test_save_enabled_on_variant_type_entry(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        create_page.enter_variant_type("TestType")

        assert create_page.is_save_button_enabled()


    # =========================================================
    # 3. TOAST WHEN VARIANT VALUE MISSING
    # =========================================================
    def test_toast_when_variant_value_missing(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        create_page.enter_variant_type("TestType")

        create_page.click_save()

        assert create_page.is_toast_message_displayed(
            "Please fill all added Variant Type and Variant Value fields."
        )


    # =========================================================
    # 4. MANUFACTURER REQUIRED
    # =========================================================
    def test_blank_manufacturer(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        # ✅ ONLY CLICK (do not select)
        create_page.click_category_dropdown()
        time.sleep(0.3)

        # ❗ IMPORTANT: your actual UI message
        assert create_page.is_transient_error_present("Please select a manufacturer first")


    # =========================================================
    # 5. CATEGORY REQUIRED
    # =========================================================
    def test_blank_category(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.enter_variant_type("Size")
        create_page.enter_variant_value("Large")

        create_page.click_save()

        # Adjust based on actual UI behavior
        assert create_page.is_error_present("Category is required") \
               or create_page.is_toast_message_displayed("Category is required")


    # =========================================================
    # 6. VARIANT TYPE REQUIRED
    # =========================================================
    def test_blank_variant_type(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category("BerlinAutomateTest")

        create_page.enter_variant_value("Large")

        create_page.click_save()

        assert create_page.is_toast_message_displayed(
            "Please fill all added Variant Type and Variant Value fields."
        )


    # =========================================================
    # 7. VARIANT VALUE REQUIRED
    # =========================================================
    def test_blank_variant_value(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        create_page.select_manufacturer("Sydneyyy Tea Shop Pvt Ltd")
        create_page.select_category("BerlinAutomateTest")

        create_page.enter_variant_type("Size")

        create_page.click_save()

        assert create_page.is_toast_message_displayed(
            "Please fill all added Variant Type and Variant Value fields."
        )


    # =========================================================
    # 8. ALL FIELDS BLANK
    # =========================================================
    def test_all_fields_blank(self, login_superadmin):
        driver = login_superadmin["driver"]
        create_page = self.open_create_page(driver)

        # IMPORTANT FIX: do NOT click save (button is disabled)
        assert create_page.is_save_button_disabled()


