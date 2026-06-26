#sentiment analysis usin quotes to scrape
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

scrape_url = os.getenv("quotes_url")
def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = [quote.text.strip() for quote in soup.find_all('span', class_='text')]
    return quotes
def analyze_sentiment(quotes):
    sentiment_analyzer = pipeline('sentiment-analysis')
    results = sentiment_analyzer(quotes)
    return results

if __name__ == "__main__":
    quotes = scrape_quotes(scrape_url)
    sentiment_results = analyze_sentiment(quotes)
    for quote, sentiment in zip(quotes, sentiment_results):
        print(f"Quote: {quote}\nSentiment: {sentiment['label']} (Score: {sentiment['score']:.2f})\n")