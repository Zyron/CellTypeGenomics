import requests
from bs4 import BeautifulSoup

def download_files_from_hpa(url, max_size_gb=1):
    # Convert the max size from GB to bytes
    max_size_bytes = max_size_gb * 1e9

    # Make an HTTP GET request to the provided URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Search for all <a> tags with the specified href structure
    links = soup.find_all('a', href=True)

    # Base URL to prepend to relative file paths
    base_url = "https://www.proteinatlas.org"

    for link in links:
        file_url = link['href']
        if file_url.endswith('.zip'):  # Check if the link is to a .zip file
            full_url = base_url + file_url

            # Check file size without downloading the entire file
            file_response = requests.head(full_url)
            file_size = int(file_response.headers.get('Content-Length', 0))

            if file_size <= max_size_bytes:
                # Download the file if it's within the size limit
                filename = file_url.split('/')[-1]  # Extract filename from the URL
                print(f"Downloading {filename}...")
                file_response = requests.get(full_url, stream=True)
                with open(filename, 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"{filename} downloaded!")
            else:
                print(f"Skipping {filename} as it exceeds the size limit.")

# Example usage
download_files_from_hpa("https://www.proteinatlas.org/about/download")
