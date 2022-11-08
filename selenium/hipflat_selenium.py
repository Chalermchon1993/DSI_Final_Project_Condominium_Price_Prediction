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
    condo_sale_price = driver.find_element(By.XPATH, "//li[@class='listing-essentials__price-item'][div[text()='For sale']]/span[@class='money']").get_attribute("data-money")
    
    # Get rent price
    try:
        condo_rent_price = driver.find_element(By.XPATH, "//li[@class='listing-essentials__price-item'][div[text()='For rent']]/span[@class='money']").get_attribute("data-money")
    except:
        condo_rent_price = driver.find_element(By.XPATH, "//li[@class='listing-essentials__price-item'][div[text()='For rent']]/span[@class='money']").text

    # Get internal features --> bedrooms, bathrooms, internal area
    internal_feature_values = []
    internal_feature_keys = []
    # Interate to get internal values
    for feature in driver.find_elements(By.XPATH, "//li[@class='listing-essentials__feature']//span[@class='number']"):
        internal_feature_values.append(feature.text)
    # Interate to get internal keys
    for feature in driver.find_elements(By.XPATH, "//li[@class='listing-essentials__feature']//div[@class='listing-essentials__feature-label']"):
        internal_feature_keys.append(feature.text)

    # Get external features --> year built, project area, towers, floors
    ## This part need to iterate and get text inside
    external_feature_values = []
    external_feature_keys = []
    # Interate to get external values
    for feature in driver.find_elements(By.XPATH, "//div[@class='text-wrapper']/span"):
        external_feature_values.append(feature.text)
    # Interate to get external values
    for feature in driver.find_elements(By.XPATH, "//div[@class='text-wrapper']/small"):
        external_feature_keys.append(feature.text)

    # Get condon description and detail
    condo_description = driver.find_element(By.XPATH, "//div[@class='property-description__content']/p[1]").text
    condo_detail = driver.find_element(By.XPATH, "//div[@class='property-description__content']/p[2]").text

    # Get condo amenities
    condo_amenity_values = []
    condo_amenity_keys = []
    # Get elements from amenity section
    condo_amenities = driver.find_elements(By.XPATH, "//ol[@class='amenities']/li")
    for feature in condo_amenities:
        condo_amenity_values.append(feature.get_attribute("class") == "amenities__item amenities__item--yes")
        condo_amenity_keys.append(feature.find_element(By.CLASS_NAME, "amenities__label").text)

    # Get neighborhood
    condo_neighbors_cats = []
    condo_neighbors_names = []
    condo_neighbors_distances = []
    condo_neighbors = driver.find_elements(By.XPATH, "//div[@class='media neighborhood-destination']")
    for i in range(len(condo_neighbors)):
        condo_neighbors_cats.append(driver.find_elements(By.XPATH, "//div[@class='media neighborhood-destination']//i")[i].get_attribute("class"))
        condo_neighbors_names.append(driver.find_elements(By.XPATH, "//div[@class='media neighborhood-destination']//h4")[i].text)
        condo_neighbors_distances.append(driver.find_elements(By.XPATH, "//div[@class='media neighborhood-destination']//small")[i].text)

    # Get market stats
    condo_stats = driver.find_elements(By.XPATH, "//ul[@class='market-data']//div[@class='indicator__amount']")
    condo_stat_asking_price_sqm = driver.find_element(By.XPATH, "//ul[@class='market-data']//span[@class='number']").text
    condo_stat_asking_price_change_quarter = condo_stats[1].text
    condo_stat_asking_price_change_year = condo_stats[2].text
    condo_stat_gross_rental_yield = condo_stats[3].text
    condo_stat_rental_price_change_year = condo_stats[4].text

    
   #### Need to check if price is existing 
   #### Test redicrect of main page

    # Test detail page scraping
    print("""
    ------------ strat scraping --------------""")
    print('developer:', condo_dev)
    print('address:', condo_address)
    print('district:', condo_district)
    print('sale price:', condo_sale_price)
    print('rental price:', condo_rent_price)
    print("""
    ------------ external features --------------""")
    for key, val in zip(external_feature_keys, external_feature_values):
        print(f"{key}: {val}")
    print("""
    ------------ internal features --------------""")
    for key, val in zip(internal_feature_keys, internal_feature_values):
        print(f"{key}: {val}")
    print("""
    ------------ internal features --------------""")
    print('description:', condo_description)
    print('detail:', condo_detail)
    print("""
    ------------ amenities --------------""")
    for key, val in zip(condo_amenity_keys, condo_amenity_values):
        print(f"{key}: {val}")
    print("""
    ------------ neighborhood --------------""")
    for cat, name, distance in zip(condo_neighbors_cats, condo_neighbors_names, condo_neighbors_distances):
        print(f"{cat}: {name}: {distance}")
    print("""
    ------------ condo stats --------------""")
    print('asking price:', condo_stat_asking_price_sqm)
    print('asking price change: quater:', condo_stat_asking_price_change_quarter)
    print('asking price change: year:', condo_stat_asking_price_change_year)
    print('gross rental yield:', condo_stat_gross_rental_yield)
    print('retal price change: year:', condo_stat_rental_price_change_year)


    time.sleep(20)