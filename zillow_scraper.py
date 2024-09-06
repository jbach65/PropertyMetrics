from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from pprint import pprint

# {'name':{'type':'int|float|ul'},{func:'convert to'}}
fields = {
    'beds': {
        'type': 'float',
        'func': 'cast_to_float',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.jritup > div > div:nth-child(1) > span.Text-c11n-8-100-2__sc-aiai24-0.styles__StyledValueText-fshdp-8-100-2__sc-12ivusx-1.bSfDch.dckbUy.--medium"
        },
    'baths': {
        'type': 'float',
        'func': 'cast_to_float',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.jritup > div > button > div > span.Text-c11n-8-100-2__sc-aiai24-0.styles__StyledValueText-fshdp-8-100-2__sc-12ivusx-1.bSfDch.dckbUy.--medium"
        },
    'sqft': {
        'type': 'int',
        'unit': 'sqft',
        'func': 'cast_to_int',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.jritup > div > div:nth-child(3) > span.Text-c11n-8-100-2__sc-aiai24-0.styles__StyledValueText-fshdp-8-100-2__sc-12ivusx-1.bSfDch.dckbUy.--medium"
        },
    'price': {
        'type': 'int',
        'unit': 'dollars',
        'func': 'price_conversion',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.bOhtbR > span > div > span > span"
        },
    'address': {
        'type': 'String',
        'func': 'address_conversion',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.bOhtbR > div > h1"
        },
    'listing age': {
        'enabled': False,
        'type': 'int',
        'unit': 'days on market',
        'func': 'listing_age_conversion',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(6) > div > div > dl > dt:nth-child(1) > strong"
        },
    'hoa': {
        'type': 'float',
        'unit': 'dollars per year',
        'func': 'hoa_conversion',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(6) > span"
        },
    'lot size': {
        'type': 'int',
        'unit': 'sqft',
        'func': 'lot_conversion',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(3) > span"
        },
    'listing type': {
        'type': 'string',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(1) > span"
        },
    'year built': {
        'type': 'int',
        'func': 'year_built_conversion',
        'selector': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(2) > span"
        }
}

def cast_to_float(s):
    try:
        f = float(s)
        return f
    except:
        return None


# if a set default is provided for this field it returns that, else None
def default_handler(item):
    if 'default' in item.keys():
        return item['default']
    else:
        return None

# Set up the Chrome WebDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Open the Zillow page
    url = "https://www.zillow.com/homedetails/6004-Elfen-Way-Austin-TX-78724/83830735_zpid/"
    driver.get(url)

    # Wait for the page to load and locate all "Show More" buttons
    show_more_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[.//span[text()="Show more"]]'))
    )

    # Loop through all "Show More" buttons unless there are more than 5... no useful info after that
    for show_more_button in show_more_buttons[0:min(5,len(show_more_buttons))]:
        try:
            # Scroll to each "Show More" button to bring it into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_button)

            # Use JavaScript to click each "Show More" button
            driver.execute_script("arguments[0].click();", show_more_button)

            # Wait to ensure content loads properly (adjust time as needed)
            time.sleep(.5)

        except Exception as e:
            print(f"Error clicking a 'Show More' button: {e}")

    # After expanding all sections, scrape the updated HTML with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Scrape desired metrics after expanding all sections
    data = {}
    for field in fields:
        # todo:: this is ugly I should fix this
        item = fields[field]

        element = soup.select(item['selector'])
        if element:
            # todo:: find a better way to handle multiple returns than just [0]
            data[field] = element[0].text
        else:
            data[field] = default_handler(item)
    pprint(data)

finally:
    # Close the browser
    driver.quit()
