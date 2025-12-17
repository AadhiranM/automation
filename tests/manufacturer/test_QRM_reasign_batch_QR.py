# import pytest
# import time
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.QR_Management.QR_management_category import QR_Management_Category_Page
# from pages.QR_Management.QR_management_QR_m_filters import QR_Management_QR_m_filters
# from utilities.customlogger import LogGen
# from pages.common.base_page import BaseTest
# from utilities.read_excel import get_test_data
#
# # Excel path
# excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
# test_data = get_test_data(excel_path, "Invalidate_QR")
#
# @pytest.mark.order(11)
# @pytest.mark.parametrize("data", test_data)
# class Test_QRM_reasign_batch_QR(BaseTest):
#     logger = LogGen.loggen()
#
#     def test_QR_management_reasign_batch_QR(self, driver, data):
#
#         search_value = data["search_value"]
#         select_status = data["select_status"]
#
#
#         self.logger.info(f"===== Invalidate QR Started | Search={search_value}, Status={select_status} =====")
#
#         # Login only once (same as products & download QR)
#         if data == test_data[0]:
#             self.driver = driver
#             self.login_and_access()
#             self.logger.info("Logged in successfully for first iteration")
#         else:
#             self.logger.info("Skipping login — already logged in")
#
#         qr_page = QR_Management_Category_Page(driver)
#         qr_page.Click_Dashboard()
#         qr_page.Click_QR_management()
#
#         qr_filters = QR_Management_QR_m_filters(driver)
#         qr_filters.Click_Qr_management()
#
#         qr_filters.Click_reset_btn()
#         qr_filters.Enter_search_field(search_value)
#         time.sleep(2)
#
#         qr_filters.select_status_drp(select_status)
#         time.sleep(2)
#         status = qr_filters.search_product(search_value)
#         if status:
#             qr_filters.click_action_btn()
#             time.sleep(1)
#             qr_filters.click_reasign_batch_QR()
#             time.sleep(1)
#             qr_filters.click_product_search()
#             time.sleep(2)
#             qr_filters.Enter_reasign_product_field(self.product)
#             time.sleep(1)
#             qr_filters.select_varinat_sku(self.varinat_sku)
#             self.logger.info(f"QR invalidated successfully for '{search_value}'")
#         else:
#             driver.save_screenshot(f".\\Screenshots\\Invalidate_No_Data_{search_value}.png")
#             self.logger.error(f"No matching data found for '{search_value}'")
#             pytest.fail(f"No matching data found for '{search_value}'")
#
#
#

import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.QR_Management.QR_management_category import QR_Management_Category_Page
from pages.QR_Management.QR_management_QR_m_filters import QR_Management_QR_m_filters
from utilities.customlogger import LogGen
from pages.common.base_page import BaseTest
from utilities.read_excel import get_test_data

# Excel path
excel_path = r"C:\Users\Suresh V\Desktop\automation\mf_products_data.xlsx"
test_data = get_test_data(excel_path, "Reassign_Batch_QR")

@pytest.mark.order(11)
@pytest.mark.parametrize("data", test_data)
class Test_QRM_reassign_batch_QR_DDT(BaseTest):
    logger = LogGen.loggen()

    def test_QR_management_reassign_batch_QR(self, driver, data):

        search_value = data["search_value"]
        select_status = data["select_status"]
        product = data["product"]
        variant_sku = data["variant_sku"]

        self.logger.info(f"===== Reassign Batch QR | Search={search_value}, Status={select_status} =====")
        # Login only once
        if data == test_data[0]:
            self.driver = driver
            self.login_and_access()
            self.logger.info("Logged in successfully for first iteration")
        else:
            self.logger.info("Skipping login — already logged in")

        qr_page = QR_Management_Category_Page(driver)
        qr_page.Click_Dashboard()
        qr_page.Click_QR_management()

        qr_filters = QR_Management_QR_m_filters(driver)
        qr_filters.Click_Qr_management()

        qr_filters.Click_reset_btn()
        qr_filters.Enter_search_field(search_value)
        time.sleep(2)

        qr_filters.select_status_drp(select_status)
        time.sleep(2)

        status = qr_filters.search_product(search_value)
        if status:
            try:
                qr_filters.click_action_btn()
                time.sleep(1)

                qr_filters.click_reasign_batch_QR()
                time.sleep(1)

                qr_filters.click_product_search()
                time.sleep(2)

                # Enter product
                qr_filters.Enter_reasign_product_field(product)
                time.sleep(2)

                # Select variant SKU
                qr_filters.select_varinat_sku(variant_sku)
                time.sleep(2)

                qr_filters.click_reasign_submit_btn()

                self.logger.info(
                    f"Batch QR reassigned successfully | Product={product}, Variant={variant_sku}"
                )

            except Exception as e:
                driver.save_screenshot(
                    f".\\Screenshots\\Reassign_Failed_{product}_{variant_sku}.png"
                )
                self.logger.error(
                    f"Reassign failed | Product='{product}', Variant='{variant_sku}' | Error: {e}"
                )
                pytest.fail(
                    f"Reassign failed: Product or Variant SKU not found "
                    f"(Product={product}, Variant={variant_sku})"
                )


