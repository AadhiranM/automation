# import time
# from selenium.webdriver import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import calendar
# import logging
# from datetime import datetime, timedelta
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from utilities.customlogger import LogGen
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
#
# class QR_Management_products_Page:
#    ## Xpath for all the elements
#     ## parent SKU
#     products= (By.XPATH, "//ul[@class='collapse-menu show']//li[3]//a[1]")
#     create_product_button=(By.XPATH,"//a[normalize-space()='Create']")
#     product_name_or_Id= (By.XPATH,"//input[@id='product_name']")
#     brand_name=(By.XPATH,"//input[@id='brand_name']")
#     products_images=(By.XPATH,"//input[@id='imageUpload']")
#     user_manual__upload_file=(By.XPATH,"//input[@id='manual-file-input']")
#     use_url=(By.XPATH,"//a[normalize-space()='Use URL']")
#     enter_manual_url=(By.XPATH,"//input[@placeholder='https://example.com/manual.pdf']")
#     product_url=(By.XPATH,"//input[@id='product_url']")
#     SKU_ID=(By.XPATH,"//input[@id='product_ref_id']")
#     drp_category=(By.XPATH,"//div[@class='choices__item choices__item--selectable']")
#     select_category=(By.XPATH,"//input[@aria-label='Select Category']")
#     drp_status=(By.XPATH,"//div[@role='listbox']//div[@class='choices__list choices__list--single']")
#     description=(By.XPATH,"//textarea[@id='product_description']")
#     country_opt=(By.XPATH,"//div[@class='ui_product-createCoo']//div[@class='choices__inner']")
#     country_of_origin=(By.XPATH,"//input[@aria-label='Select Country Of origin']")
#     regulatory_name=(By.XPATH,"//select[@id='regulatory_id']")
#     regulatory_code=(By.XPATH,"//input[@id='regulatory_codes']")
#     proceed_to_child_SKU=(By.XPATH,"//div[@class='col-md-12 text-end']//button[@id='nextButton']")
#
#     ##Child SKU
#     child_SKU=(By.XPATH,"//a[normalize-space()='Child SKU']")
#     select_variant_type_drp=(By.XPATH,"//select[@class='form-select variant-type-select']")
#     select_value=(By.XPATH,"//select[@class='form-select variant-value-select']")
#     continue_to_video_btn=(By.XPATH,"//div[@class='d-flex align-items-start gap-3 mt-4']//button[@id='nextButton']")
#
#     ##Video_details
#     video_title=(By.XPATH,"//input[@placeholder='Video Title']")
#     choose_video_file=(By.XPATH,"//input[@name='video_file[]']")
#     add_button=(By.XPATH,"//button[@id='add-video-btn']")
#     create_product_submit_button=(By.XPATH,"//button[@id='submitButton']")
#
#     #filter_details
#     search_value=(By.XPATH,"//input[@id='search-vale']")
#     filter_calender=(By.XPATH,"//input[@id='datepicker-range']")
#     filter_status=(By.XPATH,"//select[@id='idStatus']")
#     actions_icon=(By.XPATH,"//i[@class='ri-more-fill align-middle']")
#     edit_opt=(By.XPATH,"//a[normalize-space()='Edit']")
#
#
#     #filter_toggle
#     filter_toggle_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
#     product_name=(By.XPATH,"//input[@id='product_name']")
#     select_status_opt=(By.XPATH,"//div[@role='listbox']//div[@class='choices__inner']")
#     click_filter_category=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Category']")
#     Enter_category=(By.XPATH,"//input[@aria-label='Select Category']")
#     click_created_by=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Created By']")
#     Enter_created_by=(By.XPATH,"//input[@aria-label='Select Created By']")
#     click_created_date=(By.XPATH,"//input[@id='sb_date_range']")
#     aplly_btn=(By.XPATH,"//button[normalize-space()='Apply']")
#
#     #import_section
#     import_btn=(By.XPATH,"//button[normalize-space()='Import']")
#     download_sample_template_btn=(By.XPATH,"//a[normalize-space()='Download Sample Template']")
#     import_continue_btn=(By.XPATH,"//button[@id='continueToImportBtn']")
#     file_upload=(By.XPATH,"//input[@id='fileInput']")
#     import_upload_btn=(By.XPATH,"//button[@id='uploadButton']")
#
#     #import_logs_section
#     import_logs_btn=(By.XPATH,"//a[normalize-space()='Import Logs']")
#     import_log_search_value=(By.XPATH,"//input[@id='search-vale']")
#     import_log_select_date=(By.XPATH,"//input[@id='datepicker-range']")
#     import_log_status=(By.XPATH,"//select[@id='idStatus']")
#
#     imported_by_first_row = (By.XPATH, "//tbody/tr[1]/td[2]//span[@class='avatar-text copy-ellipsis-text']")
#     created_at_first_row = (By.XPATH, "//tbody/tr[1]/td[7]")
#     table_rows = (By.XPATH, "//tbody/tr")
#     search_button = (By.XPATH, "//button[.//*[name()='svg']]")
#     action_btn=(By.XPATH,"//i[@class='ri-more-fill align-middle']")
#     uploaded_file=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='Uploaded File']")
#     failed_file=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='Failed File']")
#
#
#
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 10)
#         self.logger = logging.getLogger(__name__)
#
#     # Actions
#     def Click_products(self,):
#         self.driver.find_element(*self.products).click()
#
#     def Click_create_product_button(self):
#         self.driver.find_element(*self.create_product_button).click()
#
#     def Enter_product_name_or_Id(self,product_name):
#         self.driver.find_element(*self.product_name_or_Id).clear()
#         self.driver.find_element(*self.product_name_or_Id).send_keys(product_name)
#
#     def Enter_brand_name(self,brand_name):
#         self.driver.find_element(*self.brand_name).clear()
#         self.driver.find_element(*self.brand_name).send_keys(brand_name)
#
#     # def Upload_Product_images(self,upload_product_image):
#     #     self.driver.find_element(*self.products_images).clear()
#     #     self.driver.find_element(*self.products_images).send_keys(upload_product_image)
#
#
#     def Upload_Product_images(self, upload_product_image):
#         file_input = WebDriverWait(self.driver, 10).until(
#             EC.presence_of_element_located(self.products_images)
#         )
#         self.driver.execute_script(
#             "arguments[0].value = '';",
#             file_input
#         )
#         file_input.send_keys(upload_product_image)
#
#     def User_manual_Upload_file(self,user_manual_file):
#         self.driver.find_element(*self.user_manual__upload_file).clear()
#         self.driver.find_element(*self.user_manual__upload_file).send_keys(user_manual_file)
#
#     def Enter_Product_URL(self,product_url):
#         field = self.driver.find_element(*self.product_url)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
#         self.driver.execute_script("arguments[0].value = '';", field)  # JS clear
#         field.send_keys(product_url)
#
#     def Enter_SKU_ID(self,SKU_ID):
#         self.driver.find_element(*self.SKU_ID).clear()
#         self.driver.find_element(*self.SKU_ID).send_keys(SKU_ID)
#
#     def select_category_opt(self):
#         category_opt = self.driver.find_element(*self.drp_category)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_opt)
#         time.sleep(1)
#         self.driver.execute_script("arguments[0].click();", category_opt)
#
#     def Enter_category_name(self,select_category):
#         elem=self.driver.find_element(*self.select_category)
#         elem.send_keys(select_category)
#         elem.send_keys(Keys.ENTER)
#
#     def select_status_drp(self,status):
#         # Click the dropdown container
#         dropdown = self.driver.find_element(*self.drp_status)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
#         dropdown.click()
#
#     # Wait for options to be visible and clickable
#         option_xpath = f"//div[contains(@class,'choices__list--dropdown')]//div[normalize-space()='{status}']"
#         option = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, option_xpath))
#         )
#         option.click()
#
#     def Enter_description(self,description):
#         self.driver.find_element(*self.description).clear()
#         self.driver.find_element(*self.description).send_keys(description)
#
#     def Country_option(self):
#         country_opt=self.driver.find_element(*self.country_opt)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",country_opt)
#         self.driver.execute_script("arguments[0].click();",country_opt)
#
#     def Country_of_origin(self,country):
#         ele=(self.driver.find_element(*self.country_of_origin))
#         ele.send_keys(country)
#         ele.send_keys(Keys.ENTER)
#
#     def select_regulatory_name(self,regulatory_name):
#         drp_regulatory=Select(self.driver.find_element(*self.regulatory_name))
#         drp_regulatory.select_by_visible_text(regulatory_name)
#
#     def Enter_regulatory_code(self,regulatory_code):
#         self.driver.find_element(*self.regulatory_code).clear()
#         self.driver.find_element(*self.regulatory_name).send_keys(regulatory_code)
#
#     def Click_Proceed_to_child_SKU_button(self,):
#         btn = self.driver.find_element(*self.proceed_to_child_SKU)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
#         self.driver.execute_script("arguments[0].click();", btn)
#
#     def Click_select_variant_type_drp(self,variant_type):
#         variant_type=str(variant_type)
#         select_variant_type=Select(self.driver.find_element(*self.select_variant_type_drp))
#         select_variant_type.select_by_visible_text(variant_type)
#
#     def Click_select_value_drp(self,variant_value):
#         v_value=Select(self.driver.find_element(*self.select_value))
#         v_value.select_by_visible_text(variant_value)
#
#     def Enter_video_title(self,video_title):
#         self.driver.find_element(*self.video_title).clear()
#         self.driver.find_element(*self.video_title).send_keys(video_title)
#
#     # def Choose_video_file(self,video_file):
#     #     self.driver.find_element(*self.choose_video_file).clear()
#     #     self.driver.find_element(*self.choose_video_file).send_keys(video_file)
#
#     def Choose_video_file(self, video_file):
#         file_input = WebDriverWait(self.driver,5).until(
#             EC.presence_of_element_located(self.choose_video_file)
#         )
#         # Clear existing uploaded file
#         self.driver.execute_script(
#             "arguments[0].value = '';",
#             file_input
#         )
#         # Upload new file
#         file_input.send_keys(video_file)
#
#     def ClicK_continue_video_btn(self):
#         self.driver.find_element(*self.continue_to_video_btn).click()
#
#     def Click_create_product_submit_btn(self):
#         self.driver.find_element(*self.create_product_submit_button).click()
#
#     def Enter_search_value(self,search_value):
#         self.driver.find_element(*self.search_value).send_keys(search_value)
#
#     def click_filter_calender(self):
#         self.driver.find_element(*self.filter_calender).click()
#
#     def select_filter_status(self,filter_status):
#         drp_status=Select(self.driver.find_element(*self.filter_status))
#         drp_status.select_by_visible_text(filter_status)
#
#     def select_date_range(self, start_date, end_date):
#         """
#         Flatpickr range selection
#         start_date / end_date → YYYY-MM-DD
#         """
#
#         start_year, start_month, start_day = start_date.split("-")
#         end_year, end_month, end_day = end_date.split("-")
#
#         start_month_name = calendar.month_name[int(start_month)]
#         end_month_name = calendar.month_name[int(end_month)]
#
#         calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"
#
#         self.wait.until(EC.visibility_of_element_located((By.XPATH, calendar_popup)))
#
#         # START DATE
#         year_input = self.wait.until(
#             EC.element_to_be_clickable((By.XPATH, calendar_popup + "//input[@aria-label='Year']"))
#         )
#         year_input.clear()
#         year_input.send_keys(start_year)
#
#         month_dropdown = Select(
#             self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, calendar_popup + "//select[@aria-label='Month']"))
#             )
#         )
#         month_dropdown.select_by_visible_text(start_month_name)
#         time.sleep(0.5)
#
#         for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
#             classes = d.get_attribute("class")
#             if (
#                     d.text == str(int(start_day))
#                     and "flatpickr-disabled" not in classes
#                     and "notAllowed" not in classes
#                     and "prevMonthDay" not in classes
#                     and "nextMonthDay" not in classes
#             ):
#                 d.click()
#                 break
#         time.sleep(1)
#
#         # END DATE
#         if start_year != end_year or start_month_name != end_month_name:
#             year_input.clear()
#             year_input.send_keys(end_year)
#             month_dropdown.select_by_visible_text(end_month_name)
#             time.sleep(1)
#
#         for d in self.driver.find_elements(By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"):
#
#             classes = d.get_attribute("class")
#
#             if (
#                     d.text == str(int(end_day))
#                     and "flatpickr-disabled" not in classes
#                     and "notAllowed" not in classes
#                     and "prevMonthDay" not in classes
#                     and "nextMonthDay" not in classes
#             ):
#                 d.click()
#                 break
#
#     def search_product(self,search_value):
#         flag = False
#         try:
#             # Check if table has empty message
#             empty_cells = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//td[@class='dataTables_empty']")
#             if empty_cells:
#                 print("Table is empty")
#                 return False
#
#             # Get all rows in tbody
#             rows = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//tbody//tr")
#
#             for r in range(1, len(rows) + 1):
#                 # Get product_name and batch_no using full XPath
#                 category_name = self.driver.find_element(
#                     By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"
#                 ).text.strip()
#                 product_name = self.driver.find_element(
#                     By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[3]"
#                 ).text.strip()
#
#                 sku_id = self.driver.find_element(
#                     By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[4]"
#                 ).text.strip()
#
#                 time.sleep(2)
#                 print(category_name)
#                 print(product_name)
#                 print(sku_id)
#
#                 if search_value == category_name or search_value == product_name or search_value == sku_id:
#                     flag = True
#                     break
#
#         except Exception as e:
#             print(f"Exception in searching product: {e}")
#             flag = False
#         return flag
#
#     def click_actions_icon(self):
#         self.driver.find_element(*self.actions_icon).click()
#
#     def click_edit_opt(self):
#         self.driver.find_element(*self.edit_opt).click()
#
#     def click_filter_toggle_btn(self):
#         self.driver.find_element(*self.filter_toggle_btn).click()
#
#     def Enter_filter_product_name(self,product_name):
#         self.driver.find_element(*self.product_name).send_keys(product_name)
#
#     def select_filter_toggle_status(self,filter_status):
#         # Click the dropdown container
#         dropdown = self.driver.find_element(*self.select_status_opt)
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
#         dropdown.click()
#
#     # Wait for options to be visible and clickable
#         option_xpath = f"//div[contains(@class,'choices__list--dropdown')]//div[normalize-space()='{filter_status}']"
#         option = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, option_xpath))
#         )
#         option.click()
#
#     def Enter_filter_category(self,filter_category):
#         self.driver.find_element(*self.click_filter_category).click()
#         self.driver.find_element(*self.Enter_category).send_keys(filter_category)
#         time.sleep(1)
#         self.driver.find_element(*self.Enter_category).send_keys(Keys.ENTER)
#
#     def Enter_filter_created_by(self,filter_created_by):
#         self.driver.find_element(*self.click_created_by).click()
#         self.driver.find_element(*self.Enter_created_by).send_keys(filter_created_by)
#         time.sleep(1)
#         self.driver.find_element(*self.Enter_created_by).send_keys(Keys.ENTER)
#
#     def click_filter_created_date(self):
#         self.driver.find_element(*self.click_created_date).click()
#
#     def click_apply_btn(self):
#         self.driver.find_element(*self.aplly_btn).click()
#
#     #import_section
#     def click_import_btn(self):
#         self.driver.find_element(*self.import_btn).click()
#
#     def click_download_sample_file(self):
#         self.driver.find_element(*self.download_sample_template_btn).click()
#
#     def click_import_continue_btn(self):
#         self.driver.find_element(*self.import_continue_btn).click()
#
#     def import_file_upload(self,import_file):
#         file_input = WebDriverWait(self.driver,10).until(
#             EC.presence_of_element_located(self.file_upload)
#         )
#         # Clear existing uploaded file
#         self.driver.execute_script(
#             "arguments[0].value = '';",
#             file_input
#         )
#         # Upload new file
#         file_input.send_keys(import_file)
#
#     def click_import_upload_btn(self):
#         WebDriverWait(self.driver,15).until(
#             EC.element_to_be_clickable(self.import_upload_btn)
#         ).click()
#
#
#     # Click Import Logs
#     def click_import_logs(self):
#         self.wait.until(
#             EC.element_to_be_clickable(self.import_logs_btn)
#         ).click()
#         self.logger.info("Clicked Import Logs")
#
#     # Get Imported By from first row
#     def get_imported_by_first_row(self):
#         imported_by = self.wait.until(
#             EC.visibility_of_element_located(
#                 self.imported_by_first_row
#             )
#         ).text.strip()
#
#         # Example: "A asdad" -> "asdad"
#         imported_by = imported_by.split(" ", 1)[-1]
#
#         self.logger.info(
#             f"Fetched Imported By: {imported_by}"
#         )
#         return imported_by
#
#     # Get Created At from first row
#     def get_created_at_first_row(self):
#         created_at = self.wait.until(
#             EC.visibility_of_element_located(
#                 self.created_at_first_row
#             )
#         ).text.strip()
#
#         self.logger.info(
#             f"Fetched Created At: {created_at}"
#         )
#         return created_at
#
#     # Enter Imported By
#     def enter_imported_by(self, imported_by):
#         search_box = self.wait.until(
#             EC.element_to_be_clickable(
#                 self.import_log_search_value
#             )
#         )
#         search_box.clear()
#         search_box.send_keys(imported_by)
#
#         self.logger.info(
#             f"Entered Imported By: {imported_by}"
#         )
#
#
#     # Select status
#     def select_status(self, status):
#         status_dropdown = self.wait.until(
#             EC.element_to_be_clickable(
#                 self.import_log_status
#             )
#         )
#
#         Select(status_dropdown).select_by_visible_text(status)
#
#         self.logger.info(
#             f"Selected Status: {status}"
#         )
#
#
#     def Click_action_btn(self):
#         self.wait.until(
#             EC.presence_of_element_located(
#                 self.action_btn
#             )
#         )
#
#         self.wait.until(
#             EC.element_to_be_clickable(
#                 self.action_btn
#             )
#         ).click()
#
#         self.logger.info(
#             "Clicked Action Button"
#         )
#
#
#     def is_uploaded_file_present(self):
#         try:
#             self.wait.until(EC.visibility_of_element_located(self.uploaded_file))
#             self.logger.info("Uploaded File option is present and visible")
#             return True
#         except TimeoutException:
#             self.logger.warning("Uploaded File option is not present or visible")
#             return False
#
#     def is_failed_file_present(self):
#         try:
#             self.wait.until(EC.visibility_of_element_located(self.failed_file))
#             self.logger.info("Failed File option is present and visible")
#             return True
#         except TimeoutException:
#             self.logger.warning("Failed File option is not present or visible")
#             return False
#

import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import calendar
import logging
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.customlogger import LogGen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_products_Page:
   ## Xpath for all the elements
    ## parent SKU
    dashboard= (By.XPATH, "//span[@class='nav-name'][normalize-space()='Dashboard']")
    QR_Management = (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    products= (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='Products']")
    create_product_button=(By.XPATH,"//a[normalize-space()='Create']")
    product_name_or_Id= (By.XPATH,"//input[@id='product_name']")
    brand_name=(By.XPATH,"//input[@id='brand_name']")
    products_images=(By.XPATH,"//input[@id='imageUpload']")
    user_manual__upload_file=(By.XPATH,"//input[@id='manual-file-input']")
    use_url=(By.XPATH,"//a[normalize-space()='Use URL']")
    enter_manual_url=(By.XPATH,"//input[@placeholder='https://example.com/manual.pdf']")
    product_url=(By.XPATH,"//input[@id='product_url']")
    SKU_ID=(By.XPATH,"//input[@id='product_ref_id']")
    drp_category=(By.XPATH,"//div[@class='choices__item choices__item--selectable']")
    select_category=(By.XPATH,"//input[@aria-label='Select Category']")
    drp_status=(By.XPATH,"//div[@role='listbox']//div[@class='choices__list choices__list--single']")
    description=(By.XPATH,"//textarea[@id='product_description']")
    country_opt=(By.XPATH,"//div[@class='ui_product-createCoo']//div[@class='choices__inner']")
    country_of_origin=(By.XPATH,"//input[@aria-label='Select Country Of origin']")
    regulatory_name=(By.XPATH,"//select[@id='regulatory_id']")
    regulatory_code=(By.XPATH,"//input[@id='regulatory_codes']")
    proceed_to_child_SKU=(By.XPATH,"//div[@class='col-md-12 text-end']//button[@id='nextButton']")

    ##Child SKU
    child_SKU=(By.XPATH,"//a[normalize-space()='Child SKU']")
    select_variant_type_drp=(By.XPATH,"//select[@class='form-select variant-type-select']")
    select_value=(By.XPATH,"//select[@class='form-select variant-value-select']")
    continue_to_video_btn=(By.XPATH,"//div[@class='d-flex align-items-start gap-3 mt-4']//button[@id='nextButton']")

    ##Video_details
    video_title=(By.XPATH,"//input[@placeholder='Video Title']")
    choose_video_file=(By.XPATH,"//input[@name='video_file[]']")
    add_button=(By.XPATH,"//button[@id='add-video-btn']")
    create_product_submit_button=(By.XPATH,"//button[@id='submitButton']")

    #filter_details
    search_value=(By.XPATH,"//input[@id='search-vale']")
    filter_calender=(By.XPATH,"//input[@id='datepicker-range']")
    filter_status=(By.XPATH,"//select[@id='idStatus']")
    actions_icon=(By.XPATH,"//i[@class='ri-more-fill align-middle']")
    edit_opt=(By.XPATH,"//a[normalize-space()='Edit']")


    #filter_toggle
    filter_toggle_btn=(By.XPATH,"//button[@id='filterToggleBtn']")
    product_name=(By.XPATH,"//input[@id='product_name']")
    select_status_opt=(By.XPATH,"//div[@role='listbox']//div[@class='choices__inner']")
    click_filter_category=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Category']")
    Enter_category=(By.XPATH,"//input[@aria-label='Select Category']")
    click_created_by=(By.XPATH,"//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Created By']")
    Enter_created_by=(By.XPATH,"//input[@aria-label='Select Created By']")
    click_created_date=(By.XPATH,"//input[@id='sb_date_range']")
    aplly_btn=(By.XPATH,"//button[normalize-space()='Apply']")

    #import_section
    import_btn=(By.XPATH,"//button[normalize-space()='Import']")
    download_sample_template_btn=(By.XPATH,"//a[normalize-space()='Download Sample Template']")
    import_continue_btn=(By.XPATH,"//button[@id='continueToImportBtn']")
    file_upload=(By.XPATH,"//input[@id='fileInput']")
    import_upload_btn=(By.XPATH,"//button[@id='uploadButton']")

    #import_logs_section
    import_logs_btn=(By.XPATH,"//a[normalize-space()='Import Logs']")
    import_log_search_value=(By.XPATH,"//input[@id='search-vale']")
    import_log_select_date=(By.XPATH,"//input[@id='datepicker-range']")
    import_log_status=(By.XPATH,"//select[@id='idStatus']")

    imported_by_first_row = (By.XPATH, "//tbody/tr[1]/td[2]//span[@class='avatar-text copy-ellipsis-text']")
    created_at_first_row = (By.XPATH, "//tbody/tr[1]/td[7]")
    table_rows = (By.XPATH, "//tbody/tr")
    search_button = (By.XPATH, "//button[.//*[name()='svg']]")
    action_btn=(By.XPATH,"//i[@class='ri-more-fill align-middle']")
    uploaded_file=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='Uploaded File']")
    failed_file=(By.XPATH,"//ul[@class='dropdown-menu dropdown-menu-end dd_action show']//a[@class='dropdown-item'][normalize-space()='Failed File']")



    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(__name__)

    # Actions

    def Click_Dashboard(self):
        self.wait.until(EC.element_to_be_clickable(self.dashboard)).click()

    def Click_QR_Management(self):
        self.wait.until(EC.element_to_be_clickable(self.QR_Management)).click()

    def Click_products(self,):
        self.wait.until(EC.element_to_be_clickable(self.products)).click()

    def Click_create_product_button(self):
        self.wait.until(EC.element_to_be_clickable(self.create_product_button)).click()

    def Enter_product_name_or_Id(self,product_name):
        self.wait.until(EC.element_to_be_clickable(self.product_name_or_Id)).clear()
        self.wait.until(EC.element_to_be_clickable(self.product_name_or_Id)).send_keys(product_name)

    def Enter_brand_name(self,brand_name):
        self.wait.until(EC.element_to_be_clickable(self.brand_name)).clear()
        self.wait.until(EC.element_to_be_clickable(self.brand_name)).send_keys(brand_name)

    # def Upload_Product_images(self,upload_product_image):
    #     self.wait.until(EC.element_to_be_clickable(self.products_images)).clear()
    #     self.wait.until(EC.element_to_be_clickable(self.products_images)).send_keys(upload_product_image)


    def Upload_Product_images(self, upload_product_image):
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.products_images)
        )
        self.driver.execute_script(
            "arguments[0].value = '';",
            file_input
        )
        file_input.send_keys(upload_product_image)

    def User_manual_Upload_file(self,user_manual_file):
        self.wait.until(EC.element_to_be_clickable(self.user_manual__upload_file)).clear()
        self.wait.until(EC.element_to_be_clickable(self.user_manual__upload_file)).send_keys(user_manual_file)

    def Enter_Product_URL(self,product_url):
        field = self.wait.until(EC.element_to_be_clickable(self.product_url))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        self.driver.execute_script("arguments[0].value = '';", field)  # JS clear
        field.send_keys(product_url)

    def Enter_SKU_ID(self,SKU_ID):
        self.wait.until(EC.element_to_be_clickable(self.SKU_ID)).clear()
        self.wait.until(EC.element_to_be_clickable(self.SKU_ID)).send_keys(SKU_ID)

    def select_category_opt(self):
        category_opt = self.wait.until(EC.element_to_be_clickable(self.drp_category))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_opt)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", category_opt)

    def Enter_category_name(self,select_category):
        elem=self.wait.until(EC.element_to_be_clickable(self.select_category))
        elem.send_keys(select_category)
        elem.send_keys(Keys.ENTER)

    def select_status_drp(self,status):
        # Click the dropdown container
        dropdown = self.wait.until(EC.element_to_be_clickable(self.drp_status))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        dropdown.click()

    # Wait for options to be visible and clickable
        option_xpath = f"//div[contains(@class,'choices__list--dropdown')]//div[normalize-space()='{status}']"
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        option.click()

    def Enter_description(self,description):
        self.wait.until(EC.element_to_be_clickable(self.description)).clear()
        self.wait.until(EC.element_to_be_clickable(self.description)).send_keys(description)

    def Country_option(self):
        country_opt=self.wait.until(EC.element_to_be_clickable(self.country_opt))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",country_opt)
        self.driver.execute_script("arguments[0].click();",country_opt)

    def Country_of_origin(self,country):
        ele=(self.wait.until(EC.element_to_be_clickable(self.country_of_origin)))
        ele.send_keys(country)
        ele.send_keys(Keys.ENTER)

    def select_regulatory_name(self,regulatory_name):
        drp_regulatory=Select(self.wait.until(EC.element_to_be_clickable(self.regulatory_name)))
        drp_regulatory.select_by_visible_text(regulatory_name)

    def Enter_regulatory_code(self,regulatory_code):
        self.wait.until(EC.element_to_be_clickable(self.regulatory_code)).clear()
        self.wait.until(EC.element_to_be_clickable(self.regulatory_name)).send_keys(regulatory_code)

    def Click_Proceed_to_child_SKU_button(self,):
        btn = self.wait.until(EC.element_to_be_clickable(self.proceed_to_child_SKU))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def Click_select_variant_type_drp(self,variant_type):
        variant_type=str(variant_type)
        select_variant_type=Select(self.wait.until(EC.element_to_be_clickable(self.select_variant_type_drp)))
        select_variant_type.select_by_visible_text(variant_type)

    def Click_select_value_drp(self,variant_value):
        v_value=Select(self.wait.until(EC.element_to_be_clickable(self.select_value)))
        v_value.select_by_visible_text(variant_value)

    def Enter_video_title(self,video_title):
        self.wait.until(EC.element_to_be_clickable(self.video_title)).clear()
        self.wait.until(EC.element_to_be_clickable(self.video_title)).send_keys(video_title)

    # def Choose_video_file(self,video_file):
    #     self.wait.until(EC.element_to_be_clickable(self.choose_video_file)).clear()
    #     self.wait.until(EC.element_to_be_clickable(self.choose_video_file)).send_keys(video_file)

    def Choose_video_file(self, video_file):
        file_input = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.choose_video_file)
        )
        # Clear existing uploaded file
        self.driver.execute_script(
            "arguments[0].value = '';",
            file_input
        )
        # Upload new file
        file_input.send_keys(video_file)

    def ClicK_continue_video_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.continue_to_video_btn)).click()

    def Click_create_product_submit_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.create_product_submit_button)).click()

    def Enter_search_value(self,search_value):
        self.wait.until(EC.element_to_be_clickable(self.search_value)).send_keys(search_value)

    def click_filter_calender(self):
        self.wait.until(EC.element_to_be_clickable(self.filter_calender)).click()

    def select_filter_status(self,filter_status):
        drp_status=Select(self.wait.until(EC.element_to_be_clickable(self.filter_status)))
        drp_status.select_by_visible_text(filter_status)

    def select_date_range(self, start_date, end_date):
        """
        Flatpickr range selection
        start_date / end_date → YYYY-MM-DD
        """

        start_year, start_month, start_day = start_date.split("-")
        end_year, end_month, end_day = end_date.split("-")

        start_month_name = calendar.month_name[int(start_month)]
        end_month_name = calendar.month_name[int(end_month)]

        calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"

        self.wait.until(EC.visibility_of_element_located((By.XPATH, calendar_popup)))

        # START DATE
        year_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, calendar_popup + "//input[@aria-label='Year']"))
        )
        year_input.clear()
        year_input.send_keys(start_year)

        month_dropdown = Select(
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, calendar_popup + "//select[@aria-label='Month']"))
            )
        )
        month_dropdown.select_by_visible_text(start_month_name)
        time.sleep(0.5)

        start_day_xpath = (
            calendar_popup
            + "//span[contains(@class,'flatpickr-day') and normalize-space()='"
            + str(int(start_day))
            + "' and not(contains(@class,'flatpickr-disabled'))"
            + " and not(contains(@class,'notAllowed'))"
            + " and not(contains(@class,'prevMonthDay'))"
            + " and not(contains(@class,'nextMonthDay'))]"
        )
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, start_day_xpath))
        ).click()
        time.sleep(1)

        # END DATE
        if start_year != end_year or start_month_name != end_month_name:
            year_input.clear()
            year_input.send_keys(end_year)
            month_dropdown.select_by_visible_text(end_month_name)
            time.sleep(1)

        end_day_xpath = (
            calendar_popup
            + "//span[contains(@class,'flatpickr-day') and normalize-space()='"
            + str(int(end_day))
            + "' and not(contains(@class,'flatpickr-disabled'))"
            + " and not(contains(@class,'notAllowed'))"
            + " and not(contains(@class,'prevMonthDay'))"
            + " and not(contains(@class,'nextMonthDay'))]"
        )
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, end_day_xpath))
        ).click()

    def search_product(self,search_value):
        flag = False
        try:
            # Check if table has empty message
            empty_cells = self.driver.find_elements(By.XPATH, "//table[@id='crudTable']//td[@class='dataTables_empty']")
            if empty_cells:
                print("Table is empty")
                return False

            # Get all rows in tbody
            rows = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@id='crudTable']//tbody//tr")))

            for r in range(1, len(rows) + 1):
                # Get product_name and batch_no using full XPath
                category_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[2]"))).text.strip()
                product_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[3]"))).text.strip()

                sku_id = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//table[@id='crudTable']//tbody//tr[{r}]//td[4]"))).text.strip()

                time.sleep(2)
                print(category_name)
                print(product_name)
                print(sku_id)

                if search_value == category_name or search_value == product_name or search_value == sku_id:
                    flag = True
                    break

        except Exception as e:
            print(f"Exception in searching product: {e}")
            flag = False
        return flag

    def click_actions_icon(self):
        self.wait.until(EC.element_to_be_clickable(self.actions_icon)).click()

    def click_edit_opt(self):
        self.wait.until(EC.element_to_be_clickable(self.edit_opt)).click()

    def click_filter_toggle_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.filter_toggle_btn)).click()

    def Enter_filter_product_name(self,product_name):
        self.wait.until(EC.element_to_be_clickable(self.product_name)).send_keys(product_name)

    def select_filter_toggle_status(self,filter_status):
        # Click the dropdown container
        dropdown = self.wait.until(EC.element_to_be_clickable(self.select_status_opt))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        dropdown.click()

    # Wait for options to be visible and clickable
        option_xpath = f"//div[contains(@class,'choices__list--dropdown')]//div[normalize-space()='{filter_status}']"
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        option.click()

    def Enter_filter_category(self,filter_category):
        self.wait.until(EC.element_to_be_clickable(self.click_filter_category)).click()
        self.wait.until(EC.element_to_be_clickable(self.Enter_category)).send_keys(filter_category)
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(self.Enter_category)).send_keys(Keys.ENTER)

    def Enter_filter_created_by(self,filter_created_by):
        self.wait.until(EC.element_to_be_clickable(self.click_created_by)).click()
        self.wait.until(EC.element_to_be_clickable(self.Enter_created_by)).send_keys(filter_created_by)
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(self.Enter_created_by)).send_keys(Keys.ENTER)

    def click_filter_created_date(self):
        self.wait.until(EC.element_to_be_clickable(self.click_created_date)).click()

    def click_apply_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.aplly_btn)).click()

    #import_section
    def click_import_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.import_btn)).click()

    def click_download_sample_file(self):
        self.wait.until(EC.element_to_be_clickable(self.download_sample_template_btn)).click()

    def click_import_continue_btn(self):
        self.wait.until(EC.element_to_be_clickable(self.import_continue_btn)).click()

    def import_file_upload(self,import_file):
        file_input = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located(self.file_upload)
        )
        # Clear existing uploaded file
        self.driver.execute_script(
            "arguments[0].value = '';",
            file_input
        )
        # Upload new file
        file_input.send_keys(import_file)

    def click_import_upload_btn(self):
        WebDriverWait(self.driver,15).until(
            EC.element_to_be_clickable(self.import_upload_btn)
        ).click()


    # Click Import Logs
    def click_import_logs(self):
        self.wait.until(
            EC.element_to_be_clickable(self.import_logs_btn)
        ).click()
        self.logger.info("Clicked Import Logs")

    # Get Imported By from first row
    def get_imported_by_first_row(self):
        imported_by = self.wait.until(
            EC.visibility_of_element_located(
                self.imported_by_first_row
            )
        ).text.strip()

        # Example: "A asdad" -> "asdad"
        imported_by = imported_by.split(" ", 1)[-1]

        self.logger.info(
            f"Fetched Imported By: {imported_by}"
        )
        return imported_by

    # Get Created At from first row
    def get_created_at_first_row(self):
        created_at = self.wait.until(
            EC.visibility_of_element_located(
                self.created_at_first_row
            )
        ).text.strip()

        self.logger.info(
            f"Fetched Created At: {created_at}"
        )
        return created_at

    # Enter Imported By
    def enter_imported_by(self, imported_by):
        search_box = self.wait.until(
            EC.element_to_be_clickable(
                self.import_log_search_value
            )
        )
        search_box.clear()
        search_box.send_keys(imported_by)

        self.logger.info(
            f"Entered Imported By: {imported_by}"
        )


    # Select status
    def select_status(self, status):
        status_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                self.import_log_status
            )
        )

        Select(status_dropdown).select_by_visible_text(status)

        self.logger.info(
            f"Selected Status: {status}"
        )


    def Click_action_btn(self):
        self.wait.until(
            EC.presence_of_element_located(
                self.action_btn
            )
        )

        self.wait.until(
            EC.element_to_be_clickable(
                self.action_btn
            )
        ).click()

        self.logger.info(
            "Clicked Action Button"
        )


    def is_uploaded_file_present(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.uploaded_file))
            self.logger.info("Uploaded File option is present and visible")
            return True
        except TimeoutException:
            self.logger.warning("Uploaded File option is not present or visible")
            return False

    def is_failed_file_present(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.failed_file))
            self.logger.info("Failed File option is present and visible")
            return True
        except TimeoutException:
            self.logger.warning("Failed File option is not present or visible")
            return False