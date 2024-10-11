import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer

class KeywordExtractor:
    def extract_keywords(self, pdf_path,keywords_per_page):
        text = self._extract_text_from_pdf(pdf_path)
        return self._extract_keywords_from_text(text,top_n = keywords_per_page)

    def _extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join(page.extract_text() or "" for page in reader.pages)
        return text

    def _extract_keywords_from_text(self, text, top_n):
        # Tokenize words and remove stopwords
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform([text])
        
        # Get feature names (i.e., the words) and their TF-IDF scores
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = X.toarray()[0]

        # Sort words by TF-IDF scores and return the top_n words
        sorted_indices = tfidf_scores.argsort()[-top_n:][::-1]
        top_keywords = [feature_names[i] for i in sorted_indices]
        return top_keywords
