import os
import requests
from bs4 import BeautifulSoup

# URL of the page with links to state files
url = "https://www.bls.gov/oes/tables.htm"
download_folder = "state_files"

# Create a folder to store the downloaded files if it doesn’t exist
os.makedirs(download_folder, exist_ok=True)

# Request the page and parse it
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links to Excel files (usually end with .xlsx or .xls)
for link in soup.find_all('a', href=True):
    if link['href'].endswith(('.xlsx', '.xls')):
        file_url = f"https://www.bls.gov{link['href']}"
        file_name = os.path.join(download_folder, link['href'].split('/')[-1])

        # Download the file
        file_response = requests.get(file_url)
        with open(file_name, 'wb') as file:
            file.write(file_response.content)
            print(f"Downloaded: {file_name}")