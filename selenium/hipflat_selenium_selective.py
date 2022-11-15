import os
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


def create_folder(path_name, folder_name):
    full_path = path_name + '\\' + folder_name
    isExist = os.path.exists(full_path)
    if not isExist:
        os.makedirs(full_path)
        print(f"Created folder name: {folder_name}")
    else:
        print(f"{folder_name} folder is existing.")


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



districts_dict = {
    "Bang Sue" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.SU_r2/any_p/any_b/any_a/any_w/100.52781156401632,13.819416231141265_c/14_z/list_v",
    "Bangkok Noi" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.BN_r2/any_p/any_b/any_a/any_w/100.46958041949495,13.7654879415643_c/14_z/list_v",
    "Bangkok Yai" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.BY_r2/any_p/any_b/any_a/any_w/100.47432729049152,13.738330162231323_c/14_z/list_v",
    "Don Mueang" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.DO_r2/any_p/any_b/any_a/any_w/100.59360815685145,13.926012259957446_c/14_z/list_v",
    "Huai Khwang" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.HU_r2/any_p/any_b/any_a/any_w/100.58142136980709,13.770666079379614_c/14_z/list_v",
    "Khlong Sam Wa" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KW_r2/any_p/any_b/any_a/any_w/100.73813178878407,13.876587903627952_c/14_z/list_v",
    "Lak Si" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.LS_r2/any_p/any_b/any_a/any_w/100.568662722815,13.882194328522809_c/14_z/list_v",
    "Lat Krabang" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.LK_r2/any_p/any_b/any_a/any_w/100.79233385994239,13.745093991400944_c/14_z/list_v",
    "Lat Phrao" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.LP_r2/any_p/any_b/any_a/any_w/100.60709411960012,13.82788167687477_c/14_z/list_v",
    "Min Buri" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.MI_r2/any_p/any_b/any_a/any_w/100.75361475220788,13.812562828206532_c/14_z/list_v",
    "Bueng Kum" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.BK_r2/any_p/any_b/any_a/any_w/100.64996175764422,13.812019201663777_c/14_z/list_v",
    "Din Daeng" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.DI_r2/any_p/any_b/any_a/any_w/100.56180275096828,13.777914075418758_c/14_z/list_v",
    "Dusit" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.DU_r2/any_p/any_b/any_a/any_w/100.51657256132091,13.782504558969894_c/14_z/list_v",
    "Khlong San" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KS_r2/any_p/any_b/any_a/any_w/100.50060006005295,13.726306733298014_c/14_z/list_v",
    "Prawet" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PR_r2/any_p/any_b/any_a/any_w/100.67722277222981,13.700025924964327_c/14_z/list_v",
    "Bang Khae" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KA_r2/any_p/any_b/any_a/any_w/100.39284156951082,13.719329065906035_c/14_z/list_v",
    "Bang Khen" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KE_r2/any_p/any_b/any_a/any_w/100.62956479208981,13.869665726644843_c/14_z/list_v",
    "Bang Kho Laem" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KL_r2/any_p/any_b/any_a/any_w/100.50827795401229,13.700355805950991_c/14_z/list_v",
    "Bang Na" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.NA_r2/any_p/any_b/any_a/any_w/100.62024087286072,13.670886646005284_c/14_z/list_v",
    "Bang Phlat" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PH_r2/any_p/any_b/any_a/any_w/100.49162996962619,13.786842672656212_c/14_z/list_v",
    "Nong Khaem" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.NK_r2/any_p/any_b/any_a/any_w/100.35360838341148,13.700022884766303_c/14_z/list_v",
    "Phra Khanong" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PK_r2/any_p/any_b/any_a/any_w/100.61230271353298,13.697100447229037_c/14_z/list_v",
    "Rat Burana" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.RB_r2/any_p/any_b/any_a/any_w/100.49875066039972,13.676345175343934_c/14_z/list_v",
    "Saphan Sung" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.SS_r2/any_p/any_b/any_a/any_w/100.69001841884294,13.765315260385115_c/14_z/list_v",
    "Sathon" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.ST_r2/any_p/any_b/any_a/any_w/100.52990375309344,13.717434218968057_c/14_z/list_v",
    "Taling Chan" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.TA_r2/any_p/any_b/any_a/any_w/100.43286807581691,13.772747955375655_c/14_z/list_v",
    "Thawi Watthana" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.TW_r2/any_p/any_b/any_a/any_w/100.3661124648342,13.776426815165982_c/14_z/list_v",
    "Thon Buri" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.TB_r2/any_p/any_b/any_a/any_w/100.48350989394793,13.718660612159953_c/14_z/list_v",
    "Wang Thonglang" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.WT_r2/any_p/any_b/any_a/any_w/100.60795002080745,13.7819303771441_c/14_z/list_v",
    "Watthana" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.WA_r2/any_p/any_b/any_a/any_w/100.58276002199337,13.734960866224068_c/14_z/list_v",
    "Yan Nawa" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.YA_r2/any_p/any_b/any_a/any_w/100.53950332600684,13.691945575659268_c/14_z/list_v",
    "Bang Bon" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.BO_r2/any_p/any_b/any_a/any_w/100.3878825900628,13.65931635670929_c/14_z/list_v",
    "Bang Kapi" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KP_r2/any_p/any_b/any_a/any_w/100.6385520299355,13.772725067394687_c/14_z/list_v",
    "Pathum Wan" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PA_r2/any_p/any_b/any_a/any_w/100.53467984862759,13.742768367804892_c/14_z/list_v",
    "Phasi Charoen" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PC_r2/any_p/any_b/any_a/any_w/100.43984991833749,13.726341235083112_c/14_z/list_v",
    "Phaya Thai" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PT_r2/any_p/any_b/any_a/any_w/100.54360307305902,13.784372032594588_c/14_z/list_v",
    "Phra Nakhon" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PN_r2/any_p/any_b/any_a/any_w/100.4960666457016,13.758404535018464_c/14_z/list_v",
    "Ratchathewi" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.RT_r2/any_p/any_b/any_a/any_w/100.53715809625727,13.760288984777969_c/14_z/list_v",
    "Sai Mai" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.SM_r2/any_p/any_b/any_a/any_w/100.65176504572084,13.907355630161529_c/14_z/list_v",
    "Samphanthawong" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.SA_r2/any_p/any_b/any_a/any_w/100.50753895977374,13.742357359213495_c/14_z/list_v",
    "Suan Luang" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.SL_r2/any_p/any_b/any_a/any_w/100.62684251369232,13.729958672737428_c/14_z/list_v",
    "Thung Khru" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.TK_r2/any_p/any_b/any_a/any_w/100.49638110860863,13.633891086404438_c/14_z/list_v",
    "Bang Rak" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.RA_r2/any_p/any_b/any_a/any_w/100.52302020386044,13.730336025942714_c/14_z/list_v",
    "Bang Khun Thian" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KT_r2/any_p/any_b/any_a/any_w/100.42740202168612,13.594846703739611_c/14_z/list_v",
    "Chom Thong" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.CT_r2/any_p/any_b/any_a/any_w/100.4616169803134,13.689145770966652_c/14_z/list_v",
    "Khan Na Yao" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KY_r2/any_p/any_b/any_a/any_w/100.67659588631085,13.82381161057442_c/14_z/list_v",
    "Khlong Toei" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.KH_r2/any_p/any_b/any_a/any_w/100.57090950322669,13.718172128853727_c/14_z/list_v",
    "Nong Chok" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.NC_r2/any_p/any_b/any_a/any_w/100.85800844819795,13.852829823748937_c/14_z/list_v",
    "Chatuchak" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.CH_r2/any_p/any_b/any_a/any_w/100.56387103886418,13.828960534384924_c/14_z/list_v",
    "Pom Prap Sattru Phai" : "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/TH.BM.PP_r2/any_p/any_b/any_a/any_w/100.50988913740659,13.754729235563028_c/14_z/list_v"
}


if __name__ == "__main__":

    district = 'Chom Thong'
    url = districts_dict[district]
    start_page = 16


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
    # url = "https://www.hipflat.co.th/en/search/sale/condo_y/TH.BM_r1/any_r2/any_p/any_b/any_a/any_w/100.6244261045141,13.77183154691727_c/12_z/list_v"

    full_path = "D:\TDA\DSI\projects\condominium_price_prediction\selenium\scrape_data"

    create_folder(full_path, district)

    driver.get(url)

    # Setup wait for later
    wait = WebDriverWait(driver, 10)


    # Move to the start_page
    for _ in range(start_page - 1):
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@data-role='next']")))
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[@data-role='next']").click()
    time.sleep(5)

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
    page_counter = start_page
    detail_counter = 1
    # Iterate main pages
    while next_page:
        # Get bottons link to detail pages
        detail_pages = driver.find_elements(By.CSS_SELECTOR, ".listing-information .btn-link")
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
        iterate_df.to_csv(f"{full_path}\\{district}\\hipflat_{district}_page{page_counter}.csv", encoding='utf8', index=False)
        iterate_df = template_df.copy()
        print(f"Completed {district} page {page_counter}........")

        # Check if next page exists then go to next page
        if is_next_page(driver):
            next_page = True
            page_counter += 1
            driver.find_element(By.XPATH, "//a[@data-role='next']").click()
            # Wait until next page loded
            time.sleep(3)
        else:
            next_page = False


    print(f"Completed the last page of {district}")
    driver.quit()


# Note:
# Huai Khwang start at page 16 # Done
# Bang Phlat start at page 30 # Done
# Phra Nakhon start at page 5 # Done
# Chom Thong start at page 16 # Done