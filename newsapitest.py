from newsapi import NewsApiClient

import requests
from bs4 import BeautifulSoup

def extract_article_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Failed to load article."

    soup = BeautifulSoup(response.text, 'html.parser')

    # Try extracting paragraphs (adjust tag/class for specific sites)
    paragraphs = soup.find_all('p')
    article_text = "\n".join(p.get_text() for p in paragraphs)
    
    return article_text.strip()


api = NewsApiClient(api_key='3e8305ecc71f418c8ef844ec285bbea8')

# Get data
data = api.get_top_headlines(
    #q='AI',
    #sources='bbc-news',
    category='general',       # business, entertainment, general, health, science, sports, technology
    language='en',
    country='us',
    page_size=5
)

# Sort data into articles disctionary
articles = {}
for article in data["articles"]:
    title_ascii = article["title"].encode("ascii", "ignore").decode()
    content = extract_article_text(article["url"])
    articles[title_ascii] = content

#for article in data["articles"]:
#    print(f"- {article['title'].encode("ascii", "ignore").decode()}")
#    full_text = extract_article_text(article['url'])
#    print(full_text)


