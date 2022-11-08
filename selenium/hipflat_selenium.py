import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def is_correct_page(driver): 
    try:
        driver.find_element(By.XPATH, "//div[@class='listing-essentials__transaction-label'][text()='For sale']")
        return True
    except:
        return False


def is_next_page(driver): 
    try:
        driver.find_element(By.XPATH, "//a[@data-role='next']")
        return True
    except:
        return False


def scrap_detail(driver, show_output=False):
    # Create dataframe
    header = ['dev', 'address', 'district', 'sale_price', 'rent_price', 'internal_feature_keys', 'internal_feature_values',
     'external_feature_keys', 'exteranal_feature_values', 'description', 'detail', 
     'amenity_keys', 'amenity_values',
     'neighbor_cats', 'neighbor_names', 'neighbor_distances', 'asking_price', 'asking_price_change_quater', 'asking_price_change_year', 
     'gross_rental_yield', 'rental_price_change_year']
    df = pd.DataFrame(columns=header)

    # Inner loop - get detail from each page

    try:
        condo_dev = driver.find_element(By.CLASS_NAME, "project-header-name").text
    except:
        condo_dev = None
    
    try:
        condo_address = driver.find_element(By.XPATH, "//*[@*='project-header-title']//span[1]").text
    except:
        condo_address = None
    
    try:
        condo_district = driver.find_element(By.CSS_SELECTOR, ".breadcrumb li:nth-child(2) span").text
    except:
        condo_district = None
    
    try:
        condo_sale_price = driver.find_element(By.XPATH, "//li[@class='listing-essentials__price-item'][div[text()='For sale']]/span[@class='money']").get_attribute("data-money")
    except:
        condo_sale_price = None
    
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
    try:
        condo_description = driver.find_element(By.XPATH, "//div[@class='property-description__content']/p[1]").text
    except:
        condo_description = None

    try:
        condo_detail = driver.find_element(By.XPATH, "//div[@class='property-description__content']/p[2]").text
    except:
        condo_detail = None

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
    try:
        condo_stats = driver.find_elements(By.XPATH, "//ul[@class='market-data']//div[@class='indicator__amount']")
        condo_stat_asking_price_sqm = driver.find_element(By.XPATH, "//ul[@class='market-data']//span[@class='number']").text
        condo_stat_asking_price_change_quarter = condo_stats[1].text
        condo_stat_asking_price_change_year = condo_stats[2].text
        condo_stat_gross_rental_yield = condo_stats[3].text
        condo_stat_rental_price_change_year = condo_stats[4].text
    except:
        condo_stat_asking_price_sqm = None
        condo_stat_asking_price_change_quarter = None
        condo_stat_asking_price_change_year = None
        condo_stat_gross_rental_yield = None
        condo_stat_rental_price_change_year = None

     # Create list to store each row data
    append_data = [condo_dev, condo_address, condo_district, condo_sale_price, condo_rent_price, 
    "|".join(map(str, internal_feature_keys)), "|".join(map(str, internal_feature_values)),
    "|".join(map(str, external_feature_keys)), "|".join(map(str, external_feature_values)),
    condo_description, condo_detail, 
    "|".join(map(str, condo_amenity_keys)), "|".join(map(str, condo_amenity_values)),
    "|".join(map(str, condo_neighbors_cats)), "|".join(map(str, condo_neighbors_names)), 
    "|".join(map(str, condo_neighbors_distances)), condo_stat_asking_price_sqm, condo_stat_asking_price_change_quarter,
    condo_stat_asking_price_change_year, condo_stat_gross_rental_yield, condo_stat_rental_price_change_year
    ]

    # Add data to dataframe
    df.loc[0] = append_data

    # Test detail page scraping
    if show_output == True:
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
        print('rental price change: year:', condo_stat_rental_price_change_year)

    return df




if __name__ == "__main__":

    # Add options to make selenium as human
    options = webdriver.ChromeOptions()
    options.add_argument('proxy-server=106.122.8.54:3128')
    # options.add_argument(r'--user-data-dir=C:\Users\Chalermchon Wongsopa\AppData\Local\Google\Chrome\User Data\Default')

    # Adjust window size to get the same result
    options.add_argument("--window-size=1920,1080")

    # Open website via undetected_chromedriver
    driver = uc.Chrome(options=options, version_main=102)

    # Test paths
    # driver.get("https://www.hipflat.co.th/en/listings/bangkok-condo-yzwcpndw")
    # driver.get("https://www.hipflat.co.th/projects/tait-sathorn-12-tgscll")

    # Open main page
    url = "https://www.hipflat.co.th/en/search/sale/condo,house,townhouse_y/TH.BM_r1/any_r2/any_p/any_b/any_a/any_w/100.6244261045141,13.77183154691727_c/12_z/list_v"
    driver.get(url)

    # Setup wait for later
    wait = WebDriverWait(driver, 10)

    # Store ID of the original window
    original_window = driver.current_window_handle


    # Create template dataframe
    header = ['dev', 'address', 'district', 'sale_price', 'rent_price', 'internal_feature_keys', 'internal_feature_values',
     'external_feature_keys', 'exteranal_feature_values', 'description', 'detail', 
     'amenity_keys', 'amenity_values',
     'neighbor_cats', 'neighbor_names', 'neighbor_distances', 'asking_price', 'asking_price_change_quater', 'asking_price_change_year', 
     'gross_rental_yield', 'rental_price_change_year']
    template_df = pd.DataFrame(columns=header)

    iterate_df = template_df.copy()

    next_page = True
    page_counter = 1
    detail_counter = 1
    # Iterate main pages
    while next_page:
        # Get bottons link to detail pages
        detail_pages = driver.find_elements(By.XPATH, "//a[@class='btn btn-sm btn-link']")
        # Iterate each detail page
        for page in detail_pages: 
            page.click()

            # Wait for the new window or tab
            wait.until(EC.number_of_windows_to_be(2))
            time.sleep(5)
            # Loop through until we find a new window handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            # Scrap data
            if is_correct_page(driver):
                result_df = scrap_detail(driver, show_output=False)
            
            #Close current tab
            driver.close()

            #Switch back to the old tab or window
            driver.switch_to.window(original_window)

            # Append data to dataframe
            iterate_df = pd.concat([iterate_df, result_df], ignore_index=True)
            print("Scraped item:", detail_counter)
            detail_counter += 1

        # Save file for every page
        full_path = "D:\TDA\DSI\projects\condominium_price_prediction\selenium\scrape_data"
        iterate_df.to_csv(f"{full_path}\\hipflat_page{detail_counter}.csv", index=False)
        iterate_df = template_df.copy()
        print(f"Completed page1 {page_counter}........")

        # Check if next page exists then go to next page
        if is_next_page(driver):
            next_page = True
            page_counter += 1
            driver.find_element(By.XPATH, "//a[@data-role='next']").click()
            # Wait until next page loded
            time.sleep(5)
        else:
            next_page = False


    print(f"Completed the last page. Time to make models!!!!!!!!!!!1")

    driver.quit()