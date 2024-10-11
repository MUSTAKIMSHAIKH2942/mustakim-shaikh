# from pymongo import MongoClient
# from datetime import datetime
# import logging
# from .constants import COMMON_WORDS
# from .config import MONGO_URI ,DB_NAME,KEYWORDS_STORE,META_COLLECTION
# class MongoStorage:
#     def __init__(self, db_name = DB_NAME, keyword_collection = KEYWORDS_STORE, metadata_collection = META_COLLECTION):
#         self.client = MongoClient(MONGO_URI)
#         self.db = self.client[db_name]
#         self.keyword_collection = self.db[keyword_collection]
#         self.metadata_collection = self.db[metadata_collection]

#     def store_keywords(self, pdf_name: str, keywords: list, summary: str):
#         filtered_keywords = [kw for kw in keywords if len(kw) > 2 and kw not in COMMON_WORDS]
#         document = {'pdf_name': pdf_name, 'keywords': filtered_keywords, 'summary': summary}
#         self.keyword_collection.insert_one(document)
#         logging.info(f'Stored keywords and summary for: {pdf_name}')

#     def save_metadata(self, pdf_name: str, file_path: str, file_size: int):
#         metadata_document = {
#             'pdf_name': pdf_name,
#             'file_path': file_path,
#             'file_size': file_size,
#             'ingested_at': datetime.now()
#         }
#         self.metadata_collection.insert_one(metadata_document)
#         logging.info(f'Stored metadata for: {pdf_name}')

import os
import json
from pymongo import MongoClient
from datetime import datetime
import logging
from .constants import COMMON_WORDS
from .config import MONGO_URI, DB_NAME, KEYWORDS_STORE, META_COLLECTION

class MongoStorage:
    def __init__(self, db_name=DB_NAME, keyword_collection=KEYWORDS_STORE, metadata_collection=META_COLLECTION):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[db_name]
        self.keyword_collection = self.db[keyword_collection]
        self.metadata_collection = self.db[metadata_collection]

    def store_keywords(self, pdf_name: str, keywords: list, summary: str):
        # Filter keywords and store them in the database
        filtered_keywords = [kw for kw in keywords if len(kw) > 2 and kw not in COMMON_WORDS]
        document = {'pdf_name': pdf_name, 'keywords': filtered_keywords, 'summary': summary}
        self.keyword_collection.insert_one(document)
        logging.info(f'Stored keywords and summary for: {pdf_name}')

        # After storing, retrieve the data and save it in JSON format
        self.retrieve_data_in_json_format()

    def save_metadata(self, pdf_name: str, file_path: str, file_size: int):
        metadata_document = {
            'pdf_name': pdf_name,
            'file_path': file_path,
            'file_size': file_size,
            'ingested_at': datetime.now()
        }
        self.metadata_collection.insert_one(metadata_document)
        logging.info(f'Stored metadata for: {pdf_name}')

    def retrieve_data_in_json_format(self):
        # Ensure the jsondata folder exists
        json_folder = os.path.join(os.getcwd(), 'jsondata')
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)

        # Retrieve and store keywords collection
        keyword_documents = list(self.keyword_collection.find())
        keyword_file_path = os.path.join(json_folder, 'keywords_data.json')
        with open(keyword_file_path, 'w', encoding='utf-8') as f:
            json.dump(keyword_documents, f, default=str, indent=4)
        logging.info(f'Stored keywords data in {keyword_file_path}')

        # Retrieve and store metadata collection
        metadata_documents = list(self.metadata_collection.find())
        metadata_file_path = os.path.join(json_folder, 'metadata_data.json')
        with open(metadata_file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_documents, f, default=str, indent=4)
        logging.info(f'Stored metadata data in {metadata_file_path}')
