import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re

# Function to extract the URL from logo
def extract_url(s):
    if pd.isna(s):
        return ''
    match = re.search(r"'url':\s*'([^']*)'", s)
    return match.group(1) if match else s

# Function to convert list to string
def convert_str_to_list(lst_str):
    if isinstance(lst_str, str):
        return eval(lst_str)
    return []

# Function to extract the first link from a list of links i.e. company website
def extract_website(lst_str):
    lst = convert_str_to_list(lst_str)
    for link in lst:
        if link.strip('"').startswith("http"):
            return link.strip('"')
    return ''

# Function to extract the first LinkedIn link from the list
def extract_linkedin(lst_str):
    lst = convert_str_to_list(lst_str)
    for link in lst:
        if 'www.linkedin.com' in link:
            return link.strip('"')
    return ''

# Function to extract the first Twitter link from the list
def extract_twitter(lst_str):
    lst = convert_str_to_list(lst_str)
    for link in lst:
        if 'twitter.com' in link:
            return link.strip('"')
    return ''

# Function to extract the first Facebook link from the list
def extract_facebook(lst_str):
    lst = convert_str_to_list(lst_str)
    for link in lst:
        if 'www.facebook.com' in link:
            return link.strip('"')
    return ''

# Initialize an empty DataFrame to store company information
companies = pd.DataFrame()

# URL to fetch the list of companies
url1 = "https://www.insightpartners.com/wp-json/insight/v1/get-companies"

# Loop through the pages to scrape data
for page in range(1, 65+1):
    print("Scraping Page ...", page)
    
    # Define query parameters for the request
    querystring = {"page": f"{page}", "search": "", "user_id": "", "featured_enabled": "true"}
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://www.insightpartners.com/portfolio/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    # Send GET request
    response = requests.get(url1, headers=headers, params=querystring)
    data = response.json()
    new_companies = pd.DataFrame(json.loads(data)['rows'])
    companies = pd.concat([companies, new_companies], ignore_index=True)

print(companies.head(5))

# Initialize a list to store company links
company_links = []

# Initialize lists to store all the additional fields
investment_team_list = []
sectors_list = []
tags_list = []
initial_investment_list = []
status_list = []

# URL to fetch company-specific content
url2 = "https://www.insightpartners.com/wp-json/insight/v1/get-company-content"

# Extract details from each company
for company_id in companies['id']:
    print("Scraping Company with ID: ", company_id)
    
    querystring = {"id": f"{company_id}"}
    response = requests.get(url2, params=querystring, headers=headers)
    
    decoding_json=json.loads(response.text)
    decoded_json=json.loads(decoding_json)
    html=decoded_json['content']
    
    soup = BeautifulSoup(html, 'html.parser')
    links = [link.get('href', '').replace('\\', '') for link in soup.find_all('a') if link.get('href')]
    company_links.append(list(set(links)))
    
    # Find the investment info section
    info_div = soup.find('div', class_='partnership-content__roles')
    
    if info_div:
        # Extract investment team (defaults to empty list if not found)
        team_heading = info_div.find('span', class_='font-semibold', string='Investment Team')
        if team_heading:
            company_investment_team = [member.get_text(strip=True) 
                                     for member in team_heading.find_next_siblings('span', class_='block')]
        else:
            company_investment_team=[]
            
        # Extract sectors (defaults to empty list if not found)
        sectors_heading = info_div.find('span', class_='font-semibold', string='Sectors')
        if sectors_heading:
            company_sectors = [sector.get_text(strip=True) 
                             for sector in sectors_heading.find_next_siblings('a', class_='block')]
        else:
            company_sectors = []
        
        # Extract tags (defaults to empty list if not found)
        tags_heading = info_div.find('span', class_='font-semibold', string='Tags')
        if tags_heading:
            company_tags = [tag.get_text(strip=True) 
                          for tag in tags_heading.find_next_siblings('span', class_='block')]
        else:
            company_tags = []
        
        # Extract initial investment (defaults to pd.NA if not found)
        initial_heading = info_div.find('span', class_='font-semibold', string='Initial Investment')
        if initial_heading:
            company_initial_investment = initial_heading.find_next('span', class_='block').get_text(strip=True)
        else:
            company_initial_investment = []
        
        # Extract status (defaults to pd.NA if not found)
        status_heading = info_div.find('span', class_='font-semibold', string='Status')
        if status_heading:
            company_status = status_heading.find_next('span', class_='block').get_text(strip=True)
        else:
            company_status = []
    
    # Append data to lists
    investment_team_list.append(company_investment_team)
    sectors_list.append(company_sectors)
    tags_list.append(company_tags)
    initial_investment_list.append(company_initial_investment)
    status_list.append(company_status)

companies['links'] = company_links
print(companies.head(5))

# Data Processing
companies[['slug', 'name', 'location', 'color', 'verticals', 'stage', 'logo', 'links']] = companies[
    ['slug', 'name', 'location', 'color', 'verticals', 'stage', 'logo', 'links']].astype("string")

companies['verticals'] = companies['verticals'].str.replace("'", "").str.replace("[", "").str.replace("]", "")
companies['logo'] = companies['logo'].apply(extract_url)
companies['website'] = companies['links'].apply(extract_website)
companies['linkedin'] = companies['links'].apply(extract_linkedin)
companies['twitter'] = companies['links'].apply(extract_twitter)
companies['facebook'] = companies['links'].apply(extract_facebook)
companies['location'] = companies['location'].str.replace("No Data Available, ", "")
companies['investment_team'] = investment_team_list
companies['sectors'] = sectors_list
companies['tags'] = tags_list
companies['initial_investment'] = initial_investment_list
companies['status'] = status_list

# Review Dataframe
companies
