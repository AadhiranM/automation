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

# # Excel path
# excel_path=os.path.join(os.getcwd(), r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx")
# test_data=get_test_data(excel_path, "Sheet2")  # Make sure Excel has proper columns

# @pytest.mark.order(6)
class Test_006_QR_management_QR_m_DDT(BaseTest):
    logger = LogGen.loggen()
    sku_id="PRD2025X14"
    batch_no="10"
    variant_sku_field="Black"
    quantity="10"
    manufacturing_date = "10-05-2024"  # DD-MM-YYYY
    expiry_date = "18-12-2026"  # DD-MM-YYYY
    dimension_value="2 cm"
    delivery_field_value="chennai"


    def test_QR_management_generate(self, driver):
        self.logger.info(f"===== QR Management QR Test Started for QR Generate=====")
        self.driver = driver
        self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_QR_page=QR_Management_QR_m_Page(driver)

        # Navigate to QR management
        qr_QR_page.Click_Qr_management()
        qr_QR_page.Click_generate_QR_button()
        time.sleep(2)

        # Fill product details
        qr_QR_page.click_product_skuID_opt()
        time.sleep(2)
        qr_QR_page.Enter_product_sku_field(self.sku_id)
        time.sleep(2)
        qr_QR_page.Enter_add_batch(self.batch_no)
        time.sleep(2)
        qr_QR_page.Click_variant_skuID_opt()
        qr_QR_page.Enter_varinat_sku_field(self.variant_sku_field)
        time.sleep(2)
        qr_QR_page.Enter_Quantity(self.quantity)
        time.sleep(2)
        qr_QR_page.Click_manufacturer_date()
        time.sleep(2)
        qr_QR_page.set_manufacturing_date(self.manufacturing_date)
        time.sleep(10)
        # Open calendar and select expiry date
        qr_QR_page.set_expiry_date(self.expiry_date)

        # Select Dimension and Delivery Location
        qr_QR_page.select_dimension(self.dimension_value)
        qr_QR_page.click_batch_delivery_opt()
        qr_QR_page.Enter_batch_delivery_field(self.delivery_field_value)
        time.sleep(3)
        # Generate QR
        qr_QR_page.click_genarate_QR_button()
        time.sleep(10)





