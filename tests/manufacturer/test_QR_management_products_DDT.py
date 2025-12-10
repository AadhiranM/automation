import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_products import QR_Management_products_Page
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data

# Excel path
excel_path = os.path.join(os.getcwd(),r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx")
test_data_list = get_test_data(excel_path,"Sheet1")

@pytest.mark.order(4)
class Test_004_QR_management_products_DDT(BaseTest):
    logger = LogGen.loggen()

    @pytest.mark.parametrize("data", test_data_list)
    def test_QR_management_variants_flow(self, driver, data):
        self.logger.info(f"===== QR Management products Test Started for {data['product_name']} =====")
        # self.driver = driver
        # self.login_and_access()

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_products_page = QR_Management_products_Page(driver)
        qr_products_page.Click_products()
        qr_products_page.Click_create_product_button()
        qr_products_page.Enter_product_name_or_Id(data["product_name"])
        qr_products_page.Enter_brand_name(data["brand_name"])
        time.sleep(3)
        qr_products_page.Upload_Product_images(data["upload_product_image"])
        time.sleep(3)
        qr_products_page.Enter_Product_URL(data["product_url"])
        qr_products_page.Enter_SKU_ID(data["SKU_ID"])
        time.sleep(2)

        qr_products_page.select_category_opt()
        time.sleep(1)
        qr_products_page.Enter_category_name(data["select_category"])
        time.sleep(1)
        qr_products_page.select_status_drp(data["select_status"])

        qr_products_page.Enter_description(data["description"])
        time.sleep(2)
        qr_products_page.Country_option()
        time.sleep(3)
        qr_products_page.Country_of_origin(data["country"])

        qr_products_page.Click_Proceed_to_child_SKU_button()
        time.sleep(3)

        qr_products_page.Click_select_variant_type_drp(data["variant_type"])
        time.sleep(3)
        qr_products_page.Click_select_value_drp(data["variant_value"])
        time.sleep(3)
        qr_products_page.ClicK_continue_video_btn()
        time.sleep(3)
        qr_products_page.Click_create_product_submit_btn()
        # time.sleep(3)

        try:
            WebDriverWait(driver, 25).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"),"Product created successfully!"))
            self.logger.info("Product created successfully!")
        except:
            driver.save_screenshot(".\\Screenshots\\test_create_product_scr.png")
            self.logger.error("Create product failed")
            assert False



