import requests

url = "https://newsapi.org/v2/everything"
params = {
    "q": "TikTok",
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": "3e8305ecc71f418c8ef844ec285bbea8",
    "pageSize": 100,
}
response = requests.get(url, params=params)
data = response.json()
#print(data)

for article in data["articles"]:
    print(f"- {article['title']}")
