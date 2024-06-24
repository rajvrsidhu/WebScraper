import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

companies = []

url = "https://www.eurazeo.com/en/views/ajax"

for page in range(0,0+1):
    querystring = {"_wrapper_format": "drupal_ajax"}

    payload = "view_name=portefeuille&view_display_id=block_2&view_args=&view_path=%2Fnode%2F183&view_base_path=&view_dom_id=7924bd61a25d4a337a1fed151f893322e0948f53daea3eabf952b5de3d2bf03d&pager_element=0&page=0&_drupal_ajax=1&ajax_page_state%5Btheme%5D=eurazeo&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=better_exposed_filters%2Fgeneral%2Cbetter_exposed_filters%2Fselect_all_none%2Ccore%2Fdrupal.autocomplete%2Centityreference_filter%2Fentityreference_filter%2Ceurazeo%2Feurazeo%2Ceurazeo%2Fviews_ajax_tweaks%2Cgoogle_analytics%2Fgoogle_analytics%2Clazy%2Flazy%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Csearch_api_autocomplete%2Fsearch_api_autocomplete%2Csystem%2Fbase%2Cviews%2Fviews.ajax%2Cviews%2Fviews.module%2Cviews_infinite_scroll%2Fviews-infinite-scroll"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "STYXKEY_Checkbox_Clicked=null; CookieConsent={stamp:%27pPQ1dK+6gHHcB1nwSWT9De7vTMroBwYkXBXM5+o1znMRqw5kX3nAXQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1718336042883%2Cregion:%27my%27}; _gid=GA1.2.2076044895.1719147268; _ga_JYGNSYSXQN=GS1.1.1719147266.6.1.1719148654.0.0.0; _ga=GA1.2.1505294627.1718208919; _ga_LNXY1E6BC1=GS1.1.1719147267.6.1.1719148654.0.0.0",
        "origin": "https://www.eurazeo.com",
        "priority": "u=1, i",
        "referer": "https://www.eurazeo.com/en/investments",
        "sec-ch-ua": "Not/A)Brand;v=8, Chromium;v=126, Microsoft Edge;v=126",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    response.json()
    


#store_data = [extract_store_data(div) for div in rows]
#store_data   
#print(soup.prettify()[:1000])
'''# Function to extract data from a single div
def extract_store_data(div):
    name = div.find('h3').text.strip(),
    description = div.find('p', class_='tt-4').text.strip() if div.find('p', class_='tt-4') else ''
    tag = div.find('p', class_='tag_name').text.strip() if div.find('p', class_='tag_name') else ''
    status = div.find('p', text=lambda t: t and 'Status' in t).text.replace('Status', '').strip() if div.find('p', text=lambda t: t and 'Status' in t) else ''
    investment_date = div.find('p', text=lambda t: t and 'Investment date' in t).text.replace('Investment date', '').strip() if div.find('p', text=lambda t: t and 'Investment date' in t) else ''
    sector = div.find('p', text=lambda t: t and 'Sector' in t).text.replace('Sector', '').strip() if div.find('p', text=lambda t: t and 'Sector' in t) else ''
    location = div.find('p', text=lambda t: t and 'Location' in t).text.replace('Location', '').strip() if div.find('p', text=lambda t: t and 'Location' in t) else ''
    website = div.find('a', class_='link')['href'] if div.find('a', class_='link') else ''
    return [name, description, tag, status, investment_date, sector, location, website]
'''

 # Extract HTML content from the JSON response
for item in json_data:
    if 'data' in item:
            soup = BeautifulSoup(item['data'], 'html.parser')
            rows = soup.find_all('div', class_='left-content')
            for row in rows:
                # Extract company details
                company_name = row.find('h3').text.strip() if row.find('h3') else ''
                description = row.find('p', class_='tt-4').text.strip() if row.find('p', class_='tt-4') else ''
                tag = row.find('p', class_='tag_name').text.strip() if row.find('p', class_='tag_name') else ''
                status = row.find('p', text=lambda t: t and 'Status' in t).text.replace('Status', '').strip() if row.find('p', text=lambda t: t and 'Status' in t) else ''
                investment_date = row.find('p', text=lambda t: t and 'Investment date' in t).text.replace('Investment date', '').strip() if row.find('p', text=lambda t: t and 'Investment date' in t) else ''
                sector = row.find('p', text=lambda t: t and 'Sector' in t).text.replace('Sector', '').strip() if row.find('p', text=lambda t: t and 'Sector' in t) else ''
                location = row.find('p', text=lambda t: t and 'Location' in t).text.replace('Location', '').strip() if row.find('p', text=lambda t: t and 'Location' in t) else ''
                website = row.find('a', class_='link')['href'] if row.find('a', class_='link') else ''
                
                companies.append([company_name, description, tag, status, investment_date, sector, location, website])