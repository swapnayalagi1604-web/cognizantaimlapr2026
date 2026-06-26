#scrape the site in .env

import os
import re
from dotenv import load_dotenv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
  
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

quotes_url = os.getenv("quotes_url")
language = os.getenv("language")

#create the headers 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

#read text from the url
import spacy
#python -m spacy download en_core_web_sm
# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = [quote.text.strip() for quote in soup.find_all('span', class_='text')]
    return quotes

def extract_entities(quotes):
    entities = []
    for quote in quotes:
        doc = nlp(quote)
        entities.extend([(ent.text, ent.label_) for ent in doc.ents])
    return entities
if __name__ == "__main__":
    try:
        quotes = scrape_quotes(quotes_url)
        for quote in quotes:
            print(quote)
        entities = extract_entities(quotes)
        for entity in entities:
            print(entity)
    except Exception as e:
        print(str(e))
  