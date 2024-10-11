import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'pdf_processor_db'
KEYWORDS_STORE = 'keywords'  
META_COLLECTION ='pdf_metadata'