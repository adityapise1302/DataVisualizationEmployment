import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the webpage containing the links to the data
BASE_URL = "https://www.bls.gov/oes/tables.htm"
DOWNLOAD_DIR = "bls_data"

# Create a directory to store the downloaded files
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_csv_files():
    # Get the content of the page
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links on the page
    links = soup.find_all("a", href=True)

    # Filter for "National Data" CSV files from 1997 to May 2023
    for link in links:
        href = link["href"]
        if "national" in href.lower() and href.endswith(".xlsx"):
            # Construct the full URL
            file_url = urljoin(BASE_URL, href)
            file_name = os.path.join(DOWNLOAD_DIR, href.split("/")[-1])
            
            # Download and save the file
            print(f"Downloading {file_name}...")
            try:
                file_response = requests.get(file_url)
                file_response.raise_for_status()
                with open(file_name, "wb") as file:
                    file.write(file_response.content)
                print(f"Saved {file_name}")
            except Exception as e:
                print(f"Failed to download {file_url}: {e}")

if __name__ == "__main__":
    download_csv_files()