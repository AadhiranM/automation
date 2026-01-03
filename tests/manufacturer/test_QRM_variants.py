import pytest
import time
from selenium.webdriver.common.by import By
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_variants import QR_Management_variants_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data  # your Excel utility

# Excel file containing variants data
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path,"variants")  # Sheet name: Variants

@pytest.mark.order(3)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_variants(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_variants_flow(self, driver, data):
        self.logger.info("===== QR Management Variants Test Started =====")

        # this need to enable if want to run this specific module
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Login completed for first iteration")
        else:
            self.logger.info("Skipping login — already logged in")

        category_name = data["Category"]        # Match Excel header
        variants_type = data["variants_type"]
        variants_value = data["variants_value"]

        # Navigate to QR Management (already logged in)
        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        # Variants Page
        qr_variants_page = QR_Management_variants_Page(driver)

        qr_variants_page.Click_variants()
        qr_variants_page.click_create_button()
        qr_variants_page.click_category_option()
        qr_variants_page.Enter_category_field(category_name)
        time.sleep(2)
        try:
            qr_variants_page.Click_Category_Entered_name()
        except:
            self.logger.warning(f"No category found with name '{category_name}'. Variant '{variants_value}' cannot be created.")
            assert False
            return

        # qr_variants_page.Click_Category_Entered_name()
        qr_variants_page.Enter_variants_type_field(variants_type)
        qr_variants_page.Enter_variants_value_field(variants_value)
        time.sleep(2)
        qr_variants_page.click_save_variants_button()
        time.sleep(1)

        success_msg_variant = driver.find_element(By.TAG_NAME, "body").text
        time.sleep(1)
        if "Variants saved successfully" in success_msg_variant:
            assert True
            self.logger.info(f"Variants '{variants_value}' saved successfully for category '{category_name}'")
        else:
            driver.save_screenshot(f".\\Screenshots\\test_create_variant_{variants_value}.png")
            self.logger.error(f"Create variant failed for '{variants_value}'")
            assert False
        time.sleep(3)
