import time
import calendar
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_QR_m_Page:
    ## Xpath for all the elements
    QR_Management= (By.XPATH, "//span[@class='nav-name'][normalize-space()='QR Management']")
    Qr_management = (By.XPATH, "//ul[@class='collapse-menu show']//span[@class='nav-sub-name'][normalize-space()='QR Management']")
    generate_QR_code = (By.XPATH, "//a[normalize-space()='Generate QR Code']")
    import_btn=(By.XPATH,"//button[normalize-space()='Import']")
    import_continue=(By.XPATH,"//button[@id='continueToImportBtn']")
    upload_QR_file=(By.XPATH,"//input[@id='fileInput']")
    upload_btn=(By.XPATH,"//button[@id='uploadButton']")
    product_sku_id_opt = (By.XPATH, "//div[@class='choices__item choices__placeholder choices__item--selectable'][normalize-space()='Select Product SKU ID']")
    product_sku_field=(By.XPATH,"//div[@bp-field-name='product_ref_id']//input[@name='search_terms']")
    add_batch = (By.XPATH, "//input[@placeholder='Enter Batch']")
    variant_sku_id_opt = (By.XPATH, "//div[@bp-field-name='variant_sku_id']//div[@class='choices__inner']")
    variant_sku_field = (By.XPATH, "//div[@bp-field-name='variant_sku_id']//input[@name='search_terms']")
    Quantity=(By.XPATH, "//input[@placeholder='Enter Quantity']")
    Mftr_date = (By.XPATH, "//input[@id='manufacturing_date']")
    # Fixed calendar XPaths
    date_year = (By.XPATH, "//div[contains(@class,'flatpickr-calendar')]//input[@aria-label='Year']")
    date_month = (By.XPATH, "//div[contains(@class,'flatpickr-calendar')]//select[@aria-label='Month']")
    date_days = (By.XPATH, "//div[contains(@class,'flatpickr-calendar')]//span[contains(@class,'flatpickr-day')]")
    Exp_date = (By.XPATH, "//input[@id='expiry_date']")
    Dimension=(By.XPATH,"//select[@id='dimensionDropdown']")
    batch_delivery_location_opt = (By.XPATH, "//div[@bp-field-name='batch_location']//div[@class='choices__inner']")
    batch_delivery_location_field = (By.XPATH, "//div[@bp-field-name='batch_location']//input[@name='search_terms']")
    service_drpdwn=(By.XPATH,"//select[@id='serviceDropdown']")
    genarate_QR = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------------- Actions ----------------

    def Click_QR_management(self):
        self.driver.find_element(*self.QR_Management).click()

    def Click_Qr_management(self):
        self.driver.find_element(*self.Qr_management).click()


    def Click_import_btn(self):
        self.driver.find_element(*self.import_btn).click()

    def Click_import_continue_btn(self):
        self.driver.find_element(*self.import_continue).click()

    def Click_upload_btn(self):
        self.driver.find_element(*self.upload_btn).click()

    def Enter_upload_QR_file(self,upload_file):
        self.driver.find_element(*self.upload_QR_file).send_keys(upload_file)

    def Click_generate_QR_button(self):
        self.driver.find_element(*self.generate_QR_code).click()

    def click_product_skuID_opt(self):
        self.driver.find_element(*self.product_sku_id_opt).click()

    def Enter_product_sku_field(self,sku_id):
        ele=self.driver.find_element(*self.product_sku_field)
        ele.send_keys(sku_id)
        time.sleep(2)
        ele.send_keys(Keys.ENTER)

    def Enter_add_batch(self, batch_no):
        self.driver.find_element(*self.add_batch).send_keys(batch_no)

    def Enter_Quantity(self, quantity):
        qntity=self.driver.find_element(*self.Quantity)
        qntity.clear()
        time.sleep(1)
        qntity.send_keys(quantity)
        time.sleep(2)

    def is_popup_message_present(self, expected_text):
        try:
            # Get the entire visible page text
            body_text = self.driver.find_element(By.TAG_NAME, "body").text

            if expected_text.lower() in body_text.lower():
                return True
            else:
                return False

        except Exception:
            return False

    def is_variant_field_editable(self):
        try:
            # Locate the variant input field
            element = self.driver.find_element(By.XPATH, "//div[@bp-field-name='variant_sku_id']//input[@name='search_terms']")

            # Check if element is displayed and enabled (editable)
            if element.is_displayed() and element.is_enabled():
                return True
            else:
                return False
        except:
            # Element not found → treat as not editable
            return False

    def Click_variant_skuID_opt(self):
        self.driver.find_element(*self.variant_sku_id_opt).click()

    def Enter_varinat_sku_field(self, variant_sku_field):
        variant=self.driver.find_element(*self.variant_sku_field)
        variant.send_keys(variant_sku_field)
        variant.send_keys(Keys.ENTER)

    def Click_manufacturer_date(self):
        self.driver.find_element(*self.Mftr_date).click()

    def Click_expiry_date(self):
        self.driver.find_element(*self.Exp_date).click()

    def select_date(self, date_string):
        day, month, year = date_string.split("-")
        month_name = calendar.month_name[int(month)]

        calendar_popup = "//div[contains(@class,'flatpickr-calendar') and contains(@class,'open')]"

        # YEAR
        year_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, calendar_popup + "//input[@aria-label='Year']")
            )
        )
        year_input.click()
        year_input.clear()
        year_input.send_keys(year)

        # MONTH
        month_dropdown = Select(
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, calendar_popup + "//select[@aria-label='Month']")
                )
            )
        )
        month_dropdown.select_by_visible_text(month_name)

            # DAY
        days = self.driver.find_elements(
            By.XPATH, calendar_popup + "//span[contains(@class,'flatpickr-day')]"
        )
        for d in days:
            if d.text == day and "disabled" not in d.get_attribute("class"):
                d.click()
                break
        time.sleep(2)

    def set_manufacturing_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.Mftr_date)).click()
        self.select_date(date_string)

    def set_expiry_date(self, date_string):
        self.wait.until(EC.element_to_be_clickable(self.Exp_date)).click()
        self.select_date(date_string)

    def select_dimension(self,dimension_value):
        drpdwn_dimension=Select(self.driver.find_element(*self.Dimension))
        drpdwn_dimension.select_by_visible_text(dimension_value)

    def select_service_drpdwn(self,service):
        drpdwn_service = Select(self.driver.find_element(*self.service_drpdwn))
        drpdwn_service.select_by_visible_text(service)


    def click_batch_delivery_opt(self):
        self.driver.find_element(*self.batch_delivery_location_opt).click()

    def Enter_batch_delivery_field(self,delivery_field_value):
        add=self.driver.find_element(*self.batch_delivery_location_field)
        add.clear()
        add.send_keys(delivery_field_value)
        time.sleep(2)
        add.send_keys(Keys.ENTER)

    def click_genarate_QR_button(self):
        self.driver.find_element(*self.genarate_QR).click()

