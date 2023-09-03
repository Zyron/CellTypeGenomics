import requests

def download_file(url, save_path):
    """
    Download a file from a given URL and save it to a specified path.
    
    Args:
    - url (str): The URL of the file to be downloaded.
    - save_path (str): The local path where the file should be saved.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad responses
    
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

# Example usage:
# Assuming you've identified the exact URL of the file you want
file_url = "https://www.proteinatlas.org/path/to/your/file.extension"
local_path = "path_where_you_want_to_save_the_file.extension"

download_file(file_url, local_path)
