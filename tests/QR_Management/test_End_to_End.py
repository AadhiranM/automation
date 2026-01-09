# import pytest
# import time
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# from pages.common.AccessCodePage import AccessCodePage
# from pages.QR_Management.login_page import Loginpage
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_Management.QR_management_variants import QR_Management_variants_Page
# from pages.QR_Management.QR_management_products import QR_Management_products_Page
# from pages.QR_Management.QR_management_QR_m import QR_Management_QR_m_Page
# from pages.QR_Management.QR_management_QR_m_filters import QR_Management_QR_m_filters
#
# from pages.common.base_page import BaseTest
# from utilities.readproperties import Readconfig
# from utilities.customlogger import LogGen
# from utilities.read_excel import get_test_data
#
# excel_path_products = os.path.join(os.getcwd(), r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx")
# product_data_list = get_test_data(excel_path_products, "Sheet1")
# qr_data_list = get_test_data(excel_path_products, "Sheet2")
# upload_file_path = r"C:\Users\Suresh V\Downloads\qr-import-sample (1).xlsx"
#
#
# @pytest.mark.order(1)
# class Test_EndToEnd_QR_Flow(BaseTest):
#     logger = LogGen.loggen()
#
#     category_name = "airpods"
#     category_status = "Active"
#     variant_type = "colour"
#     variant_value = "black"
#     search_value = "earbuds"
#     select_status = "Completed"
#
#     def test_end_to_end_flow(self, driver):
#         self.driver = driver
#         self.logger.info("=== E2E Flow: START ===")
#
#         # -------------------------
#         # 1) LOGIN + ACCESS CODE
#         # -------------------------
#         ac_page = AccessCodePage(driver)
#         ac_page.enter_access_code(Readconfig.getAccessCode())
#         time.sleep(2)
#
#         lp = Loginpage(driver)
#         lp.setUserName(Readconfig.getUsername())
#         lp.setPassword(Readconfig.getUserpassword())
#         lp.clickLogin()
#         self.logger.info("Login successful")
#
#         # -------------------------
#         # 2) CREATE CATEGORY
#         # -------------------------
#         qr_page = QR_Management_Category_Page(driver)
#         qr_page.Click_QR_management()
#         qr_page.click_category()
#         qr_page.click_create_category_button()
#         qr_page.Enter_category_value(self.category_name)
#         qr_page.click_category_status(self.category_status)
#         qr_page.click_save_button()
#         time.sleep(1)
#
#         msg_category = driver.find_element(By.TAG_NAME, "body").text
#         if "Category Created Successfully!" in msg_category:
#             self.logger.info("Category created successfully")
#         else:
#             driver.save_screenshot(".\\Screenshots\\category_failed.png")
#             self.logger.error("Category creation failed")
#             # assert False
#
#         # -------------------------
#         # 3) CREATE VARIANTS
#         # -------------------------
#         qr_page.Click_Dashboard()
#         qr_page.Click_QR_management()
#
#         variants_page = QR_Management_variants_Page(driver)
#         variants_page.Click_variants()
#         variants_page.click_create_button()
#         variants_page.click_category_option()
#         variants_page.Enter_category_field(self.category_name)
#         time.sleep(1)
#         variants_page.Click_Category_Entered_name()
#         variants_page.Enter_variants_type_field(self.variant_type)
#         variants_page.Enter_variants_value_field(self.variant_value)
#         time.sleep(1)
#         variants_page.click_save_variants_button()
#         time.sleep(1)
#
#         msg_variant = driver.find_element(By.TAG_NAME, "body").text
#         if "Variants saved successfully" in msg_variant:
#             self.logger.info("Variants saved successfully")
#         else:
#             driver.save_screenshot(".\\Screenshots\\variant_failed.png")
#             self.logger.error("Variants creation failed")
#             # assert False
#
#         # -------------------------
#         # 4) CREATE PRODUCTS
#         # -------------------------
#         products_page = QR_Management_products_Page(driver)
#         products_page.Click_products()
#         time.sleep(1)
#
#         for data in product_data_list:
#             products_page.Click_create_product_button()
#             time.sleep(1)
#             products_page.Enter_product_name_or_Id(data["product_name"])
#             products_page.Enter_brand_name(data["brand_name"])
#             time.sleep(1)
#             products_page.Upload_Product_images(data["upload_product_image"])
#             time.sleep(1)
#             products_page.Enter_Product_URL(data["product_url"])
#             products_page.Enter_SKU_ID(data["SKU_ID"])
#             time.sleep(1)
#             products_page.select_category_opt()
#             products_page.Enter_category_name(data["select_category"])
#             products_page.select_status_drp(data["select_status"])
#             products_page.Enter_description(data["description"])
#             products_page.Country_option()
#             products_page.Country_of_origin(data["country"])
#             products_page.Click_Proceed_to_child_SKU_button()
#             time.sleep(1)
#             products_page.Click_select_variant_type_drp(data["variant_type"])
#             products_page.Click_select_value_drp(data["variant_value"])
#             products_page.ClicK_continue_video_btn()
#             products_page.Click_create_product_submit_btn()
#
#             try:
#                 WebDriverWait(driver, 25).until(
#                     EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Product created successfully!")
#                 )
#                 self.logger.info(f"Product {data['product_name']} created successfully")
#             except:
#                 driver.save_screenshot(".\\Screenshots\\product_failed.png")
#                 self.logger.error(f"Product creation failed for {data['product_name']}")
#                 assert False
#
#         # -------------------------
#         # 5) GENERATE QR
#         # -------------------------
#         qr_page.Click_Dashboard()
#         qr_page.Click_QR_management()
#         qr_m_page = QR_Management_QR_m_Page(driver)
#
#         for data in qr_data_list:
#             qr_m_page.Click_Qr_management()
#             qr_m_page.Click_generate_QR_button()
#             time.sleep(1)
#             qr_m_page.click_product_skuID_opt()
#             qr_m_page.Enter_product_sku_field(data["sku_id"])
#             qr_m_page.Enter_add_batch(data["batch_no"])
#             qr_m_page.Click_variant_skuID_opt()
#             time.sleep(1)
#
#             if not qr_m_page.is_variant_field_editable():
#                 self.logger.info("Existing batch detected → skipping editable fields")
#                 qr_m_page.Enter_Quantity(data["quantity"])
#                 qr_m_page.click_genarate_QR_button()
#             else:
#                 qr_m_page.Enter_varinat_sku_field(data["variant_sku"])
#                 qr_m_page.Enter_Quantity(data["quantity"])
#                 qr_m_page.Click_manufacturer_date()
#                 qr_m_page.set_manufacturing_date(data["manufacturing_date"])
#                 qr_m_page.set_expiry_date(data["expiry_date"])
#                 qr_m_page.select_dimension(data["dimension"])
#                 qr_m_page.click_batch_delivery_opt()
#                 qr_m_page.Enter_batch_delivery_field(data["delivery_location"])
#                 qr_m_page.click_genarate_QR_button()
#
#             try:
#                 WebDriverWait(driver, 25).until(
#                     EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "QR Generation successfully initiated!")
#                 )
#                 self.logger.info(f"QR generated successfully for SKU {data['sku_id']}")
#             except:
#                 driver.save_screenshot(".\\Screenshots\\QR_failed.png")
#                 self.logger.error(f"QR generation failed for SKU {data['sku_id']}")
#                 assert False
#
#         # -------------------------
#         # 6) IMPORT QR FILE
#         # -------------------------
#         qr_m_page.Click_Qr_management()
#         qr_m_page.Click_import_btn()
#         qr_m_page.Click_import_continue_btn()
#         qr_m_page.Enter_upload_QR_file(upload_file_path)
#         qr_m_page.Click_upload_btn()
#         try:
#             WebDriverWait(driver, 25).until(
#                 EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "QR import initiated successfully.")
#             )
#             self.logger.info("QR import file processed successfully")
#             time.sleep(5)
#         except:
#             driver.save_screenshot(".\\Screenshots\\QR_import_failed.png")
#             self.logger.error("QR import failed")
#             assert False
#
#         # -------------------------
#         # 7) FILTER QR
#         # -------------------------
#         qr_filter_page = QR_Management_QR_m_filters(driver)
#         qr_filter_page.Click_Qr_management()
#         qr_filter_page.Click_reset_btn()
#         qr_filter_page.Enter_search_field(self.search_value)
#         qr_filter_page.Click_search_btn()
#         time.sleep(2)
#
#         status = qr_filter_page.search_product(self.search_value)
#         assert status == True
#         self.logger.info("QR filter search successful")
#         self.logger.info("=== E2E Flow: COMPLETED ===")
#
#
#
#
