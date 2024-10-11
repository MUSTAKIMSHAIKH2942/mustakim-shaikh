import os
import logging
from .db import MongoStorage
from .extractor import KeywordExtractor
from .summarizer import ML_Summarizer
import PyPDF2

def get_number_of_pages(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)
        # Calculate top_n based on the number of pages (e.g., 10 keywords per page)
        top_n = num_pages * 5
        return top_n

def process_pdf(file_path):
    title = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    mongo_storage = MongoStorage()
    mongo_storage.save_metadata(title, file_path, file_size)

    try:
        # Get the number of pages and calculate top_n
        top_n = get_number_of_pages(file_path)

        keyword_extractor = KeywordExtractor()
        keywords = keyword_extractor.extract_keywords(file_path, keywords_per_page=top_n)  # Adjust keywords_per_page as needed

        summarizer = ML_Summarizer()
        summary = summarizer.summarize(file_path, keywords)

        mongo_storage.store_keywords(title, keywords, summary)

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
