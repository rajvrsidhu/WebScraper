import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re

# Function to extract the URL from the string
def extract_url(s):
    match = re.search(r"'url':\s*'([^']*)'", s)
    return match.group(1) if match else s

# Function to extract the first link from a list of links i.e. company website
def extract_website(lst):
    if isinstance(lst, list) and len(lst) > 0:
        return lst[0].strip('"')
    return ''

# Function to extract the first LinkedIn link from the list
def extract_linkedin(lst):
    if isinstance(lst, list):
        for link in lst:
            if 'www.linkedin.com' in link:
                return link.strip('"')
    return ''

# Function to extract the first Twitter link from the list
def extract_twitter(lst):
    if isinstance(lst, list):
        for link in lst:
            if 'twitter.com' in link:
                return link.strip('"')
    return ''

# Function to extract the first Facebook link from the list
def extract_facebook(lst):
    if isinstance(lst, list):
        for link in lst:
            if 'www.facebook.com' in link:
                return link.strip('"')
    return ''

# Initialize an empty DataFrame to store company information
companies = pd.DataFrame()

# URL to fetch the list of companies
url1 = "https://www.insightpartners.com/wp-json/insight/v1/get-companies"

# Loop through the pages to scrape data
for page in range(1, 43 + 1):
    print("Scraping ...", page)
    
    # Define query parameters for the request
    querystring = {"status[]": "Current Investment", "page": f"{page}", "search": "", "user_id": "", "featured_enabled": "true"}

    # Define request headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "...",  # Truncated for brevity
        "priority": "u=1, i",
        "referer": "https://www.insightpartners.com/portfolio/",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    # Send GET request to fetch company data
    response = requests.get(url1, headers=headers, params=querystring)

    # Parse the JSON response
    data = response.json()
    
    # Convert the 'rows' field in the JSON response to a DataFrame
    new_companies = pd.DataFrame(data['rows'])
    
    # Append the new company data to the main DataFrame
    companies = pd.concat([companies, new_companies], ignore_index=True)

# Display the companies DataFrame
print(companies)

# Initialize a list to store company links
company_links = []

# URL to fetch company-specific content
url2 = "https://www.insightpartners.com/wp-json/insight/v1/get-company-content"

# Loop through each company ID to fetch detailed information
for id in companies['id']:
    print("Scraping ...", id)
    
    # Define query parameters for the request
    querystring = {"id": f"{id}"}

    # Send GET request to fetch company-specific content
    response = requests.get(url2, params=querystring, headers=headers)
    
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags in the response
    links = soup.find_all('a')

    # Initialize a list to store unique links
    unique_links = []
    for link in links:
        href = link.get('href')
        if href is not None:
            href = href.replace('\\', '')  # Remove backslashes
            if href not in unique_links:
                unique_links.append(href)
                
    # Append the unique links to the company_links list
    company_links.append(unique_links)

# Add the company links to the DataFrame
companies['links'] = company_links
print(companies.info())

# Clean and process DataFrame columns
companies['verticals'] = companies['verticals'].str.replace("'", "")
companies['logo'] = companies['logo'].apply(extract_url)
companies['website'] = companies['links'].apply(extract_website)
companies['linkedin'] = companies['links'].apply(extract_linkedin)
companies['twitter'] = companies['links'].apply(extract_twitter)
companies['facebook'] = companies['links'].apply(extract_facebook)

# Display the first 10 rows of the DataFrame
print(companies.head(10))

# Export the DataFrame to an Excel file
companies.to_excel(r"C:\Users\RajveerSingh\OneDrive - 2X LLC\Workspcace VS Code\GitHub Repos\Insight Partners Web Scraping\Companies.xlsx", index=False)

# Uncomment the following lines to convert specific columns to 'object' type and display DataFrame info
'''
test = companies
test[['slug', 'name', 'location', 'color', 'verticals', 'stage', 'logo', 'Links']] = test[['slug', 'name', 'location', 'color', 'verticals', 'stage', 'logo', 'Links']].astype(object)
test.info()
'''