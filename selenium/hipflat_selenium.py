import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

if __name__ == "__main__":

    # Add options to make selenium as human
    options = webdriver.ChromeOptions()
    # options.add_argument('proxy-server=106.122.8.54:3128')
    options.add_argument(r'--user-data-dir=C:\Users\Chalermchon Wongsopa\AppData\Local\Google\Chrome\User Data\Default')

    # Open website via undetected_chromedriver
    driver = uc.Chrome(options=options)
    driver.get("https://www.hipflat.co.th/en/listings/bangkok-condo-yzwcpndw")

    # Inner loop - get detail from each page
    condo_dev = driver.find_element(By.CLASS_NAME, "project-header-name").text
    condo_address = driver.find_element(By.XPATH, "//*[@*='project-header-title']//span[1]").text
    condo_district = driver.find_element(By.CSS_SELECTOR, ".breadcrumb li:nth-child(2) span").text
    condo_sub_vals = driver.find_elements(By.XPATH, "//div[@class='text-wrapper']/span")
    condo_sub_keys = driver.find_elements(By.XPATH, "//div[@class='text-wrapper']/small")
    
   #### Need to check if price is existing 
   #### Test redicrect of main page

    print('developer:', condo_dev)
    print('address:', condo_address)
    print('district:', condo_district)
    for key, val in zip(condo_sub_keys, condo_sub_vals):
        print(key.text, val.text)
    time.sleep(20)
