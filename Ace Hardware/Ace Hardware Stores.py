import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract store data from a div element
def extract_store_data(div):
    parts = div.find_all("div")
    name = parts[0].find("a")["title"].strip()
    address = parts[1].text.strip()
    location = parts[2].text.strip()
    phone = parts[3].text.strip()
    return [name, address, location, phone]

# Website URL
url = "https://www.acehardware.com/store-directory"

# Define the headers to send with the HTTP request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

# Send a GET request to the URL with the specified headers
response = requests.request("GET", url, headers=headers) #requests.get is viable

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all div elements with the relevant class for store data
rows = soup.find_all('div', class_='col-xs-12 col-sm-6 col-md-3 store-directory-list-item')

# Extract the store data from each div element using the extract_store_data function
store_data = [extract_store_data(div) for div in rows]

# Create a pandas dataframe from the extracted store data
header=['Name','Address line 1','Address line 2','Phone Number']
df_store_data=pd.DataFrame(store_data)
df_store_data.columns=header

# Print the resulting dataframe
df_store_data

# Export the DataFrame to an Excel file
df_store_data.to_excel(r"C:\Users\RajveerSingh\OneDrive - 2X LLC\Workspcace VS Code\GitHub Repos\WebScraper\Ace Hardware\Stores.xlsx",index=False)
