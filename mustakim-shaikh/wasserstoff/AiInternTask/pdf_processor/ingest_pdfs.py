import os
import logging
import requests
from PyPDF2 import PdfReader  # Ensure this import matches your actual usage
from .process_pdf import process_pdf

def get_dynamic_folder(pdf_path):
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    
    if num_pages <= 10:
        return 'Short_PDFs'
    elif 10 < num_pages <= 30:
        return 'Medium_PDFs'
    else:
        return 'Long_PDFs'

# Process PDFs from local folder
def ingest_pdfs_from_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            folder_type = get_dynamic_folder(pdf_path)
            dynamic_folder = os.path.join(folder_path, folder_type)

            # Ensure dynamic folder exists
            os.makedirs(dynamic_folder, exist_ok=True)

            # Check if the PDF already exists in the destination folder
            new_pdf_path = os.path.join(dynamic_folder, file_name)
            if os.path.exists(new_pdf_path):
                logging.info(f"Skipped: {file_name} already exists in {folder_type}")
                continue  # Skip this file if it already exists

            # Move PDF to appropriate folder
            os.rename(pdf_path, new_pdf_path)
            logging.info(f"Moved: {file_name} to {folder_type}")
            process_pdf(new_pdf_path)

# Download and process PDFs from URLs
def ingest_pdfs_from_urls(pdf_urls, download_folder):
    for pdf_name, url in pdf_urls.items():
        pdf_path = os.path.join(download_folder, f"{pdf_name}.pdf")

        # Check if the PDF already exists before downloading
        if os.path.exists(pdf_path):
            logging.info(f"Skipped: {pdf_name} already exists in {download_folder}")
            continue  # Skip downloading if the file already exists

        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(response.content)

            logging.info(f"Downloaded: {pdf_name}")

            folder_type = get_dynamic_folder(pdf_path)
            dynamic_folder = os.path.join(download_folder, folder_type)

            # Ensure dynamic folder exists
            os.makedirs(dynamic_folder, exist_ok=True)

            # Move PDF to appropriate folder
            new_pdf_path = os.path.join(dynamic_folder, f"{pdf_name}.pdf")
            if os.path.exists(new_pdf_path):
                logging.info(f"Skipped: {pdf_name} already exists in {folder_type}")
                continue  # Skip this file if it already exists

            os.rename(pdf_path, new_pdf_path)
            logging.info(f"Moved: {pdf_name} to {folder_type}")
            process_pdf(new_pdf_path)

        except Exception as e:
            logging.error(f"Failed to download {pdf_name}: {e}")
