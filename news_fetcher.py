import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("NEWSAPI_API_KEY")

from newsapi import NewsApiClient

import requests
from bs4 import BeautifulSoup

def extract_article_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}          # Looks like normal request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to load article."

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = "\n".join(p.get_text() for p in paragraphs)
    
    return article_text.strip()

def get_articles(category='general'):
    api = NewsApiClient(api_key=api_key)

    # Get data
    data = api.get_top_headlines(
        #q='AI',
        #sources='bbc-news',
        category=category,       # business, entertainment, general, health, science, sports, technology
        language='en',
        country='us',
        page_size=5
    )

    # Sort data and urls into articles and urls disctionary
    articles = {}
    urls = {}
    for article in data["articles"]:
        title_ascii = article["title"].encode("ascii", "ignore").decode()
        content = extract_article_text(article["url"])
        articles[title_ascii] = content
        urls[title_ascii] = article["url"]

    return articles, urls