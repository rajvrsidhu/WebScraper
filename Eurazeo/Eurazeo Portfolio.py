import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Initialize an empty list to store company data
companies = []

# URL for the AJAX request
url = "https://www.eurazeo.com/en/views/ajax"

# Loop through each page (0 to 37)
for page in range(0, 37+1):
    print("Scraping Page ...", page)
    
    # Query string parameters
    querystring = {"_wrapper_format": "drupal_ajax"}
    
    # Payload data for the POST request
    payload = {
        "view_name": "portefeuille",
        "view_display_id": "block_2",
        "view_args": "",
        "view_path": "/node/183",
        "view_base_path": "",
        "view_dom_id": "7924bd61a25d4a337a1fed151f893322e0948f53daea3eabf952b5de3d2bf03d",
        "pager_element": "0",
        "page": f"{page}",  # Current page number
        "_drupal_ajax": "1",
        "ajax_page_state[theme]": "eurazeo",
        "ajax_page_state[theme_token]": "",
        "ajax_page_state[libraries]": "better_exposed_filters/general,better_exposed_filters/select_all_none,core/drupal.autocomplete,entityreference_filter/entityreference_filter,eurazeo/eurazeo,eurazeo/views_ajax_tweaks,google_analytics/google_analytics,lazy/lazy,paragraphs/drupal.paragraphs.unpublished,search_api_autocomplete/search_api_autocomplete,system/base,views/views.ajax,views/views.module,views_infinite_scroll/views-infinite-scroll"
    }
    
    # Request headers
    headers = {
        "accept": "application/json, string/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "STYXKEY_Checkbox_Clicked=null; CookieConsent={stamp:%27pPQ1dK+6gHHcB1nwSWT9De7vTMroBwYkXBXM5+o1znMRqw5kX3nAXQ==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1718336042883%2Cregion:%27my%27}; _gid=GA1.2.2076044895.1719147268; _ga_JYGNSYSXQN=GS1.1.1719147266.6.1.1719148654.0.0.0; _ga=GA1.2.1505294627.1718208919; _ga_LNXY1E6BC1=GS1.1.1719147267.6.1.1719148654.0.0.0",
        "origin": "https://www.eurazeo.com",
        "priority": "u=1, i",
        "referer": "https://www.eurazeo.com/en/investments",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    
    # Send the POST request
    response = requests.post(url, data=payload, headers=headers, params=querystring)
    
    # Parse the JSON response
    json_data = response.json()
    
    # Extract HTML content from the JSON response
    for item in json_data:
        if 'data' in item:
            soup = BeautifulSoup(item['data'], 'html.parser')
            rows = soup.find_all('div', class_='left-content')
            for row in rows:
                # Extract company details
                company_name = row.find('h3').string.strip() if row.find('h3') else ''
                description = row.find('p', class_='tt-4').string.strip() if row.find('p', class_='tt-4') else ''
                tag = row.find('p', class_='tag_name').string.strip() if row.find('p', class_='tag_name') else ''
                # Extract additional information from the txt-wrap div
                txt_wrap_div = row.find('div', class_='txt-wrap')
                if txt_wrap_div:
                    status = txt_wrap_div.find('strong', string='Status').next_sibling.strip() if txt_wrap_div.find('strong', string='Status') else ''
                    investment_date = txt_wrap_div.find('strong', string='Investment date').next_sibling.strip() if txt_wrap_div.find('strong', string='Investment date') else ''
                    sector = txt_wrap_div.find('strong', string='Sector').next_sibling.strip() if txt_wrap_div.find('strong', string='Sector') else ''
                    location = txt_wrap_div.find('strong', string='Location').next_sibling.strip() if txt_wrap_div.find('strong', string='Location') else ''
                # Extract website URL from the link tag
                website = row.find('a', class_='link')['href'] if row.find('a', class_='link') else ''
                # Append the extracted information to the companies list
                companies.append([company_name, description, tag, status, investment_date, sector, location, website])

# Convert to DataFrame
companies = pd.DataFrame(companies, columns=['Company Name', 'Description', 'Tag', 'Status', 'Investment Date', 'Sector', 'Location', 'Website'])
all_companies = companies
# Filter to only thos that are in the current portfolio
companies = companies[companies['Status']=="In portfolio"]

# Export the DataFrame to an Excel file
companies.to_excel(r"C:\Users\RajveerSingh\OneDrive - 2X LLC\Workspcace VS Code\GitHub Repos\WebScraper\Eurazeo\Companies.xlsx",index=False)
