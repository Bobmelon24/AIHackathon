from newsapi import NewsApiClient

api = NewsApiClient(api_key='3e8305ecc71f418c8ef844ec285bbea8')

data = api.get_top_headlines(
    q='AI',
    #sources='bbc-news',
    category='general',       # business, entertainment, general, health, science, sports, technology
    language='en',
    country='us',
    page_size=5
)

for article in data["articles"]:
    print(f"- {article['title'].encode("ascii", "ignore").decode()}")

