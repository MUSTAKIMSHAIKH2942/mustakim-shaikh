import re
import PyPDF2
from nltk.tokenize import sent_tokenize

class ML_Summarizer:
    def summarize(self, pdf_path, keywords):
        # Extract text and number of pages from the PDF
        text, num_pages = self._extract_text_from_pdf(pdf_path)

        # Check if text is empty
        if not text:
            print(f"Warning: No text extracted from {pdf_path}.")
            return f"No text extracted from {pdf_path}."

        # Tokenize text into sentences
        sentences = sent_tokenize(text)

        # Calculate keyword density for each sentence
        keyword_density = self._calculate_keyword_density(sentences, keywords)

        # Sort sentences based on keyword density in descending order
        sorted_sentences = sorted(keyword_density, key=lambda x: x[1], reverse=True)

        # Dynamically adjust the number of sentences to include in the summary
        summary_sentences = self._determine_summary_length(sorted_sentences, num_pages)

        # Return the final summary as a single string
        return " ".join(sentence for sentence, _ in summary_sentences)

    def _extract_text_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''.join(page.extract_text() or "" for page in reader.pages)
                num_pages = len(reader.pages)

            # Log the number of pages and extracted text
            print(f"Extracted {num_pages} pages from {pdf_path}.")
            return text, num_pages

        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return "", 0  # Return empty text and zero pages on error

    def _calculate_keyword_density(self, sentences, keywords):
        keyword_density = []
        for sentence in sentences:
            # Convert the sentence to lowercase and find all words
            words = re.findall(r'\b\w+\b', sentence.lower())
            if not words:
                continue  # Skip empty sentences

            # Calculate keyword density (number of keywords / total words)
            keyword_count = sum(1 for word in words if word in keywords)
            density = keyword_count / len(words)

            # Add the sentence to the list if it contains meaningful content
            if keyword_count > 0:  # Ensures that the sentence has keywords
                keyword_density.append((sentence, density))

        return keyword_density

    def _determine_summary_length(self, sorted_sentences, num_pages):
        # Define how many sentences to include in the summary based on document length
        # Adjust sentences per page based on your requirement
        sentences_per_page = 5  # For shorter documents
        if num_pages <= 10:
            sentences_per_page = 6  # 1 sentence per page for short documents
        elif num_pages <= 50:
            sentences_per_page = 5  # 2 sentences per page for medium documents
        elif num_pages <= 100:
            sentences_per_page = 4  # 3 sentences per page for larger documents
        else:
            sentences_per_page = 4  # 5 sentences per page for very large documents

        max_summary_sentences = min(sentences_per_page * num_pages, len(sorted_sentences))

        # For short documents, return at least a few sentences
        if max_summary_sentences < 8:
            max_summary_sentences = min(5, len(sorted_sentences))  # Ensure at least 5 sentences for short docs

        # Return the top sentences by keyword density
        return sorted_sentences[:max_summary_sentences]
