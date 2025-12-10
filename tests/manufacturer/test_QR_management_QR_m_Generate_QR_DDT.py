import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page  # Your POM
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data

excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path,"Sheet2")

@pytest.mark.order(5)
@pytest.mark.parametrize("data", test_data)
class Test_005_QR_management_QR_m_DDT(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_generate(self, driver, data):
        self.logger.info("===== QR Management QR Test Started =====")
        # self.driver = driver
        # self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_QR_page = QR_Management_QR_m_Page(driver)

        # Navigate to QR management
        qr_QR_page.Click_Qr_management()
        qr_QR_page.Click_generate_QR_button()
        time.sleep(2)

        # Fill product details
        qr_QR_page.click_product_skuID_opt()
        qr_QR_page.Enter_product_sku_field(data["sku_id"])
        qr_QR_page.Enter_add_batch(data["batch_no"])
        time.sleep(2)
        qr_QR_page.Click_variant_skuID_opt()
        time.sleep(2)

        if qr_QR_page.is_popup_message_present("Batch number already exists for a different product."):
            screenshot_path = ".\\screenshots\\Batch_Id_error.png"
            driver.save_screenshot(screenshot_path)
            self.logger.error("Popup detected: Batch ID already exists!")
            pytest.exit("Batch number exists - please change the Batch number  ")

        # Detect autofill by checking if field is editable
        if not qr_QR_page.is_variant_field_editable():
            self.logger.info("Existing batch detected → fields are disabled → Skipping form entry.")
            qr_QR_page.Enter_Quantity(data["quantity"])
            qr_QR_page.click_genarate_QR_button()

            try:
                WebDriverWait(driver, 25).until(
                    EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "QR Generation successfully initiated!")
                )
                self.logger.info("QR Generated Successfully for Existing Batch!")
            except:
                driver.save_screenshot(".\\Screenshots\\test_QR_generated_failed_existing_batch.png")
                self.logger.error("QR generation failed for existing batch")
                assert False
            return  # Stop further actions for existing batch
        time.sleep(1)
        # ONLY for new products (editable fields)
        qr_QR_page.Enter_varinat_sku_field(data["variant_sku"])
        time.sleep(1)
        qr_QR_page.Enter_Quantity(data["quantity"])
        time.sleep(1)

        # Dates
        qr_QR_page.Click_manufacturer_date()
        time.sleep(1)
        qr_QR_page.set_manufacturing_date(data["manufacturing_date"])
        time.sleep(1)
        qr_QR_page.set_expiry_date(data["expiry_date"])
        time.sleep(1)

        # Dropdowns
        qr_QR_page.select_dimension(data["dimension"])
        time.sleep(1)
        qr_QR_page.click_batch_delivery_opt()
        qr_QR_page.Enter_batch_delivery_field(data["delivery_location"])
        time.sleep(1)

        # Generate QR
        qr_QR_page.click_genarate_QR_button()
        try:
            WebDriverWait(driver, 25).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"),"QR Generation successfully initiated!"))
            self.logger.info("QR Generated successfully!")
            time.sleep(10)
        except:
            driver.save_screenshot(".\\Screenshots\\test_QR generated_failed_scr.png")
            self.logger.error("QR generated failed")
            assert False

        time.sleep(10)
