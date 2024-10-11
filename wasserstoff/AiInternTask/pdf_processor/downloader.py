import os
import requests
import re

# Function to sanitize the filename
def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to download PDF from URL
def download_pdf(url, folder_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        # Get the PDF filename from the URL
        filename = url.split("/")[-1]
        sanitized_filename = sanitize_filename(filename)  # Sanitize the filename
        pdf_path = os.path.join(folder_path, sanitized_filename)
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        return pdf_path
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None
