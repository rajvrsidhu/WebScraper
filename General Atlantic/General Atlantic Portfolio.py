import requests
import pandas as pd
from bs4 import BeautifulSoup
import itertools

# Define a function to extract company details from a BeautifulSoup object
def company_details(soup):
    name = [elem.text.strip().replace(' ×', '') for elem in soup.find_all('h3', class_='grid-item--accordion-title')]
    sector = [li.find('span').text for li in soup.find_all('li') if 'Sector:' in li.text]
    headquarters = [li.find('span').text for li in soup.find_all('li') if 'Headquarters:' in li.text]
    invested_date = [li.find('span').text for li in soup.find_all('li') if 'Date Invested:' in li.text]
    website = [li.find('a')['href'] for li in soup.find_all('li') if li.find('a') and 'Visit Website' in li.text]
    # Return a list of tuples containing the extracted company details
    return list(itertools.zip_longest(name, sector, headquarters, invested_date, website))

# Initialize an empty list to store the extracted company data
company_extract = []

# Define the URL and payload for the POST request
url = "https://www.generalatlantic.com/wp-admin/admin-ajax.php"

# Loop through each page (1 to 15)
for page in range(1,15+1):
    print("Scraping Page ...", page)
    # Construct the payload for the current page
    payload = f"action=get_ajax_content&data%5Bfilter_search%5D=&data%5Bfilter_type%5D=current&data%5Bfilter_sector%5D=&data%5Bfilter_region%5D=&data%5Bfilter_year%5D=&data%5Bfilter_location%5D=&data%5Bfilter_cats%5D%5B%5D=current&data%5Bfilter_cats%5D%5B%5D=&data%5Bfilter_cats%5D%5B%5D=&data%5Bfilter_cats%5D%5B%5D=&data%5Bfilter_cats%5D%5B%5D=&data%5Bcontent%5D=portfolio&data%5Bnext%5D=-1&data%5Bpaged%5D={page}"

    # Define the headers for the POST request
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM3MDY2NTIiLCJhcCI6IjExMjAxMzMwNDIiLCJpZCI6ImQyMjczYjNmZDdkZmQxYzgiLCJ0ciI6ImM3ZTQ4Nzk1OTQwNDg0YmIyNWVhMzM4NDY2ZmM4YzczIiwidGkiOjE3MTkyNDE5OTQ0NTYsInRrIjoiNjY2ODYifX0=",
        "origin": "https://www.generalatlantic.com",
        "priority": "u=1, i",
        "referer": "https://www.generalatlantic.com/portfolio/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "traceparent": "00-c7e48795940484bb25ea338466fc8c73-d2273b3fd7dfd1c8-01",
        "tracestate": "66686@nr=0-1-3706652-1120133042-d2273b3fd7dfd1c8----1719241994456",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "x-newrelic-id": "VwEHV1BWChABVFdbAwkEV1IE",
        "x-requested-with": "XMLHttpRequest"
    }

    # Send the POST request
    response = requests.post(url, data=payload, headers=headers)

    # Parse the JSON response
    json_data = response.json()

    # Extract HTML content from the JSON response
    soup = BeautifulSoup(json_data['posts'], 'html.parser')
    rows = soup.find_all('div',_class="grid-item--accordion-meta")
    company_extract.extend(company_details(soup))
    
# Create a DataFrame from the collected data
companies = pd.DataFrame(company_extract, columns=['Name', 'Sector', 'Headquarters', 'Date Invested', 'Website'])
companies
# Export the DataFrame to an Excel file
companies.to_excel(r"C:\Users\RajveerSingh\OneDrive - 2X LLC\Workspcace VS Code\GitHub Repos\WebScraper\General Atlantic\Companies.xlsx",index=False)