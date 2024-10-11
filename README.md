
## Task: Domain-Specific PDF Summarization & Keyword Extraction Pipeline

## Objective
The goal of this project is to develop a dynamic pipeline that processes multiple PDF documents from a desktop folder, generates domain-specific summaries and keywords, and stores them in a MongoDB database. The pipeline should manage documents of varying lengths and update the database efficiently after processing each document.

## Features
PDF Ingestion & Parsing: The system can process PDFs from a folder (short, medium, and long documents).
Concurrency & Performance: Parallel processing ensures efficiency and optimal resource management for handling multiple files.
Summarization: Generates content-based summaries based on the length and domain of each PDF.
Keyword Extraction: Extracts non-generic, domain-specific keywords that accurately reflect the document's content.
MongoDB Storage: Stores initial metadata and updates with the generated summary and keywords.
Error Handling: Logs errors such as corrupted files or unsupported formats while maintaining database integrity.
## Installation & Setup
1. System Requirements
Python 3.8+
MongoDB 4.0+
Git

2. Environment Setup
Clone the repository:

git clone https://github.com/MUSTAKIMSHAIKH2942/mustakim-shaikh.git

cd AiInternTask

## Create a virtual environment:

python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

## Install dependencies:
pip install -r requirements.txt

![Directory Structure Pic](https://github.com/MUSTAKIMSHAIKH2942/mustakim-shaikh/blob/main/lpp_for_pdf_processor.PNG)
## Setup environment variables:

## Create a .env file in the root folder.
env

MONGO_URI=mongodb://localhost:27017                                                                                              
DATABASE_NAME=pdf_processing                                                                                                      
PDF_FOLDER_PATH=your_pdf_folder_path                                                                                              
Start MongoDB: Ensure MongoDB is running locally or update the MONGO_URI in your .env file to connect to a remote MongoDB instance.
                                                                                                                                  
## Run the pipeline:
## Run the main script:

python main.py


## Usage Guide

## PDF Ingestion:

Place the PDFs in the folder specified in the .env file.
The pipeline will process documents of varying lengths (1-10 pages for short, 10-30 pages for medium, and 30+ pages for long).

## Summarization & Keyword Extraction:

The pipeline dynamically generates summaries and keywords for each PDF based on its content and length.
Ensure your PDFs are domain-specific for optimal keyword relevance.
MongoDB Integration:

## After processing each document, the pipeline will store the document's metadata (name, path, size) in MongoDB.
Once the summaries and keywords are generated, the database entry for each document is updated.


## Performance:

The system supports parallel processing for efficient handling of large PDF batches.
Benchmark results for concurrency and processing speed can be found in the output folder.
Docker Setup (Optional)
Build Docker Image:


docker build -t pdf_pipeline .
## Run Docker Container:                  

docker run -d -p 5000:5000 --env-file .env pdf_pipeline


Error Handling & Logging

All errors (e.g., corrupted files) are logged in the output/logs folder, ensuring the pipeline continues uninterrupted.
MongoDB records are only updated once valid summaries and keywords are generated.
## Performance Reports
Performance data such as time per document and resource usage can be generated by enabling the profiling feature in main.py.


