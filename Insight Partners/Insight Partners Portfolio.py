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
companies=pd.DataFrame()

# URL to fetch the list of companies
url1 = "https://www.insightpartners.com/wp-json/insight/v1/get-companies"

# Loop through the pages to scrape data
for page in range(1,43+1):
    print("Scraping Page ...",page)
    
    # Define query parameters for the request
    querystring = {"status[]":"Current Investment","page":f"{page}","search":"","user_id":"","featured_enabled":"true"}

    # Define request headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "_biz_uid=d5c3bd72c38e4c61c58f92991edd4f99; _mkto_trk=id:936-JAF-209&token:_mch-insightpartners.com-1718181682785-77787; _biz_flagsA=%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _gd_visitor=0aeb5227-5c53-48f7-84cc-08f727698571; sliguid=f27a4d0d-b7e2-4f26-9b1d-0daa85b4ca28; slirequested=true; _hjSessionUser_2846427=eyJpZCI6IjgzYWUxYmYxLWZmZGYtNTRhNy05NmUxLTdlYjcyY2VjZTgyNCIsImNyZWF0ZWQiOjE3MTgxODE2ODQ3MTcsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.582262255.1718181683; _hjSession_2846427=eyJpZCI6ImIyYWQ5ODI2LWQ4ZTEtNDY0Zi1iNGUzLTZiMjdmY2UzZmViZSIsImMiOjE3MTkwNjI4OTk1MTAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; slireg=https://scout.us1.salesloft.com; _gd_session=a79d5bb9-71c4-47a9-88af-e2e217fd88bb; _ga_R6M33R23CY=GS1.1.1719062899.14.1.1719062910.0.0.0; _biz_nA=94; _biz_pendingA=%5B%5D",
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
    string = response.json()
    data = json.loads(string)
    
    # Convert the 'rows' field in the JSON response to a DataFrame
    new_companies=pd.DataFrame(data['rows'])
    
    # Append the new company data to the main DataFrame
    companies=pd.concat([companies,new_companies],ignore_index=True)
    
    
# Display the companies DataFrame
print(companies.head(5))

# Initialize a list to store company links
company_links = []

# URL to fetch company-specific content
url2 = "https://www.insightpartners.com/wp-json/insight/v1/get-company-content"

# Loop through each company ID to fetch detailed information
for id in companies['id']:
    print("Scraping Company with ID: ",id)
    
    # Define query parameters for the request
    querystring = {"id":f"{id}"}

    #payload = ""
    # Define request headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "_biz_uid=d5c3bd72c38e4c61c58f92991edd4f99; _mkto_trk=id:936-JAF-209&token:_mch-insightpartners.com-1718181682785-77787; _biz_flagsA=%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _gd_visitor=0aeb5227-5c53-48f7-84cc-08f727698571; sliguid=f27a4d0d-b7e2-4f26-9b1d-0daa85b4ca28; slirequested=true; _hjSessionUser_2846427=eyJpZCI6IjgzYWUxYmYxLWZmZGYtNTRhNy05NmUxLTdlYjcyY2VjZTgyNCIsImNyZWF0ZWQiOjE3MTgxODE2ODQ3MTcsImV4aXN0aW5nIjp0cnVlfQ==; _ga=GA1.1.582262255.1718181683; _hjSession_2846427=eyJpZCI6ImIyYWQ5ODI2LWQ4ZTEtNDY0Zi1iNGUzLTZiMjdmY2UzZmViZSIsImMiOjE3MTkwNjI4OTk1MTAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; slireg=https://scout.us1.salesloft.com; _gd_session=a79d5bb9-71c4-47a9-88af-e2e217fd88bb; _biz_nA=90; _ga_R6M33R23CY=GS1.1.1719062899.14.1.1719062910.0.0.0; _biz_pendingA=%5B%5D",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    # Send GET request to fetch company-specific content
    response = requests.get(url2, params=querystring, headers=headers)
    
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags in the response
    links = soup.find_all('a')

    # Initialize a list to store unique links
    unique_links=[]
    for link in links:
        href = link.get('href')
        if href is not None:
            href = href.replace('\\', '')  # Remove backslashes
            if href not in unique_links:
                unique_links.append(href)
    
    # Append the unique links to the company_links list            
    company_links.append(unique_links)
            
# Add the company links to the DataFrame   
companies['links']=company_links
print(companies.head(5))
print(companies.info())
test=companies

# Change variable types for the dataframe
companies[['slug','name','location','color','verticals','stage','logo','links']]=companies[['slug','name','location','color','verticals','stage','logo','links']].astype("string")

# Clean and process DataFrame columns
companies['verticals'] = companies['verticals'].str.replace("'","").str.replace("[","").str.replace("]","")
companies['logo']=companies['logo'].apply(extract_url)
companies['website']=companies['links'].apply(extract_website)
companies['linkedin']=companies['links'].apply(extract_linkedin)
companies['twitter']=companies['links'].apply(extract_twitter)
companies['facebook']=companies['links'].apply(extract_facebook)
companies['location']=companies['location'].str.replace("No Data Available, ","")

# Print the resulting dataframe
companies