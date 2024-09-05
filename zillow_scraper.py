import requests
from bs4 import BeautifulSoup
from pprint import pprint

# Zillow URLs
url = "https://www.zillow.com/homedetails/6004-Elfen-Way-Austin-TX-78724/83830735_zpid/"
#url = "https://www.zillow.com/homedetails/12206-Donington-Dr-Austin-TX-78753/29435220_zpid/"

# Set headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
}

fields = {
    'beds': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.jritup > div > div:nth-child(1) > span.Text-c11n-8-100-2__sc-aiai24-0.styles__StyledValueText-fshdp-8-100-2__sc-12ivusx-1.bSfDch.dckbUy.--medium",
    'baths': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.jritup > div > button > div > span.Text-c11n-8-100-2__sc-aiai24-0.styles__StyledValueText-fshdp-8-100-2__sc-12ivusx-1.bSfDch.dckbUy.--medium",
    'sqft': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.jritup > div > div:nth-child(3) > span.Text-c11n-8-100-2__sc-aiai24-0.styles__StyledValueText-fshdp-8-100-2__sc-12ivusx-1.bSfDch.dckbUy.--medium",
    'price': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.bOhtbR > span > div > span > span",
    'address': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(2) > div > div > div > div > div > div > div.Flex-c11n-8-100-2__sc-n94bjd-0.bOhtbR > div > h1",
    'listing age': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(6) > div > div > dl > dt:nth-child(1) > strong",
    'hoa': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(6) > span",
    'lot size': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(3) > span",
    'listing type': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(1) > span",
    'year built': "#search-detail-lightbox > div.sc-eBOGjE.cXYlOv > div:nth-child(2) > div.styles__StyledContentWrapper-fshdp-8-100-2__sc-112i4yx-0.eoYEXG.layout-wrapper > div.layout-container-desktop > div.layout-content-container > div.layout-static-column-container > div > div > div:nth-child(4) > div > div > div > div:nth-child(2) > span"
}


response = requests.get(url, headers=headers)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}
    for field in fields:
        element = soup.select_one(fields[field])
        if element:
            data[field] = element.text
        else:
            data[field] = None
    pprint(data)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
