import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

scrape_url = os.getenv("lyrics_url")

headers = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_lyrics(url):
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    lyrics_div = soup.find("pre", class_="lyric-body")

    if lyrics_div:
        return lyrics_div.get_text(separator="\n").strip()

    raise Exception("Lyrics not found on page.")


def split_lyrics(lyrics):
    lines = lyrics.split("\n")

    docs = [
        line.strip()
        for line in lines
        if len(line.strip()) > 5
    ]

    return docs


def topic_modeling(lyrics):
    docs = split_lyrics(lyrics)

    if len(docs) < 2:
        raise Exception("Need at least 2 lyric lines for topic modeling.")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        lowercase=True
    )

    X = vectorizer.fit_transform(docs)

    n_topics = min(3, len(docs))

    model = NMF(
        n_components=n_topics,
        random_state=42
    )

    model.fit(X)

    words = vectorizer.get_feature_names_out()

    print("\nDiscovered Topics:")

    for topic_index, topic in enumerate(model.components_):
        top_words = topic.argsort()[-5:][::-1]

        print(f"\nTopic {topic_index + 1}:")
        for i in top_words:
            print(words[i])


if __name__ == "__main__":
    try:
        lyrics = scrape_lyrics(scrape_url)

        print("\nLyrics:")
        print(lyrics)

        topic_modeling(lyrics)

    except Exception as e:
        print(f"Error: {e}")