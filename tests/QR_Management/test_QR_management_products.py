# import pytest
# import time
# from selenium.webdriver.common.by import By
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_Management.QR_management_variants import QR_Management_variants_Page
# from utilities.customlogger import LogGen
# from pages.QR_Management.QR_management_products import QR_Management_products_Page
# from pages.common.base_page import BaseTest
#
# # @pytest.mark.order(4)
# class Test_004_QR_management_products(BaseTest):
#     logger = LogGen.loggen()
#
#     product_name="Sample Electric Kettle"
#     brand_name="TechNova"
#     upload_product_image=r"C:\Users\Suresh V\Desktop\automation\lena-denk-vO_RghTzvxE-unsplash(1).jpg"
#     user_manual_file=""
#     product_url="https://example.com/products/sample-electric-kettle"
#     SKU_ID="PRD2025X9"
#     select_category="electicalkettle"
#     select_status="Active"
#     description="A high-quality product designed for durability and everyday use"
#     country="India"
#     regulatory_name=""
#     regulatory_code=""
#
#     ##child SKU
#     variant_type="1102"
#     variant_value="black"
#
#     def test_QR_management_variants_flow(self, driver):
#         self.logger.info("===== QR Management products Test Started =====")
#         #### this need to enable if want to run this specific module
#         self.driver = driver
#         self.login_and_access()
#
#         #Navigate to QR Management (already logged in from Category test)
#         qr_page = QR_Management_Category_Page(driver)
#         qr_page.Click_Dashboard()
#         qr_page.Click_QR_management()
#
#         # Variants Page
#         qr_products_page = QR_Management_products_Page(driver)
#         qr_products_page.Click_products()
#         qr_products_page.Click_create_product_button()
#         qr_products_page.Enter_product_name_or_Id(self.product_name)
#         qr_products_page.Enter_brand_name(self.brand_name)
#         qr_products_page.Upload_Product_images(self.upload_product_image)
#         time.sleep(5)
#         # qr_products_page.User_manual_Upload_file(self.user_manual_file)
#         qr_products_page.Enter_Product_URL(self.product_url)
#         qr_products_page.Enter_SKU_ID(self.SKU_ID)
#         time.sleep(3)
#
#         qr_products_page.select_category_opt()
#         time.sleep(2)
#         qr_products_page.Enter_category_name(self.select_category)
#         time.sleep(2)
#         qr_products_page.select_status_drp(self.select_status)
#
#         qr_products_page.Enter_description(self.description)
#         time.sleep(3)
#         qr_products_page.Country_option()
#         qr_products_page.Country_of_origin(self.country)
#         # qr_products_page.select_regulatory_name(self.regulatory_name)
#         # qr_products_page.Enter_regulatory_code(self.regulatory_code)
#         qr_products_page.Click_Proceed_to_child_SKU_button()
#         time.sleep(3)
#         # qr_products_page.child_SKU()
#         qr_products_page.Click_select_variant_type_drp(self.variant_type)
#         qr_products_page.Click_select_value_drp(self.variant_value)
#         qr_products_page.ClicK_continue_video_btn()
#         qr_products_page.Click_create_product_submit_btn()
#         time.sleep(1)
#
