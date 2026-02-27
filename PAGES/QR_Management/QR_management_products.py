import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QR_Management_products_Page:
   ## Xpath for all the elements
    ## parent SKU
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
    drp_category=(By.XPATH,"//div[@class='mb-3']//div[@class='choices__inner']")
    select_category=(By.XPATH,"//input[@aria-label='Select Category']")
    drp_status=(By.XPATH,"//select[@id='product_status']")
    description=(By.XPATH,"//textarea[@id='product_description']")
    country_opt=(By.XPATH,"//div[@class='mb-3 ui_product-createCoo']//div[@class='choices__inner']")
    country_of_origin=(By.XPATH,"//input[@aria-label='Select Country']")
    regulatory_name=(By.XPATH,"//select[@id='regulatory_id']")
    regulatory_code=(By.XPATH,"//input[@id='regulatory_codes']")
    proceed_to_child_SKU=(By.XPATH,"//div[@class='col-md-12 text-end']//button[@id='nextButton']")

    ##Child SKU
    child_SKU=(By.XPATH,"//a[normalize-space()='Child SKU']")
    select_variant_type_drp=(By.XPATH,"//select[@class='form-select variant-type-select']")
    select_value=(By.XPATH,"//select[@class='form-select variant-value-select']")
    continue_to_video_btn=(By.XPATH,"//div[@class='d-flex align-items-start gap-3 mt-4']//button[@id='nextButton']")

    ##Video_details
    video_title=(By.XPATH,"//input[@id='newVideoTitle']")
    choose_video_file=(By.XPATH,"//input[@id='newVideoFile']")
    add_button=(By.XPATH,"//button[@id='add-video-btn']")
    create_product_submit_button=(By.XPATH,"//button[@id='submitButton']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Actions
    def Click_products(self,):
        self.driver.find_element(*self.products).click()

    def Click_create_product_button(self):
        self.driver.find_element(*self.create_product_button).click()

    def Enter_product_name_or_Id(self,product_name):
        self.driver.find_element(*self.product_name_or_Id).send_keys(product_name)

    def Enter_brand_name(self,brand_name):
        self.driver.find_element(*self.brand_name).send_keys(brand_name)

    def Upload_Product_images(self,upload_product_image):
        self.driver.find_element(*self.products_images).send_keys(upload_product_image)

    def User_manual_Upload_file(self,user_manual_file):
        self.driver.find_element(*self.user_manual__upload_file).send_keys(user_manual_file)

    def Enter_Product_URL(self,product_url):
        # self.driver.find_element(*self.product_url).clear()
        # self.driver.find_element(*self.product_url).send_keys(product_url)
        field = self.driver.find_element(*self.product_url)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        self.driver.execute_script("arguments[0].value = '';", field)  # JS clear
        field.send_keys(product_url)

    def Enter_SKU_ID(self,SKU_ID):
        self.driver.find_element(*self.SKU_ID).clear()
        self.driver.find_element(*self.SKU_ID).send_keys(SKU_ID)

    def select_category_opt(self):
        category_opt = self.driver.find_element(*self.drp_category)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_opt)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", category_opt)

    def Enter_category_name(self,select_category):
        elem=self.driver.find_element(*self.select_category)
        elem.send_keys(select_category)
        elem.send_keys(Keys.ENTER)

    def select_status_drp(self,select_status):
        drpdwn_status=Select(self.driver.find_element(*self.drp_status))
        drpdwn_status.select_by_visible_text(select_status)

    def Enter_description(self,description):
        self.driver.find_element(*self.description).send_keys(description)

    def Country_option(self):
        country_opt=self.driver.find_element(*self.country_opt)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",country_opt)
        self.driver.execute_script("arguments[0].click();",country_opt)


    def Country_of_origin(self,country):
        ele=(self.driver.find_element(*self.country_of_origin))
        ele.send_keys(country)
        ele.send_keys(Keys.ENTER)

    def select_regulatory_name(self,regulatory_name):
        drp_regulatory=Select(self.driver.find_element(*self.regulatory_name))
        drp_regulatory.select_by_visible_text(regulatory_name)

    def Enter_regulatory_code(self,regulatory_code):
        self.driver.find_element(*self.regulatory_name).send_keys(regulatory_code)

    def Click_Proceed_to_child_SKU_button(self,):
        btn = self.driver.find_element(*self.proceed_to_child_SKU)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def Click_select_variant_type_drp(self,variant_type):
        variant_type=str(variant_type)
        select_variant_type=Select(self.driver.find_element(*self.select_variant_type_drp))
        select_variant_type.select_by_visible_text(variant_type)

    def Click_select_value_drp(self,variant_value):
        v_value=Select(self.driver.find_element(*self.select_value))
        v_value.select_by_visible_text(variant_value)

    def ClicK_continue_video_btn(self):
        self.driver.find_element(*self.continue_to_video_btn).click()

    def Click_create_product_submit_btn(self):
        self.driver.find_element(*self.create_product_submit_button).click()








