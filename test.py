import requests
from bs4 import BeautifulSoup

def fetch_latest_tweets(account, count=5):
    url = f"https://mobile.twitter.com/{account.strip('@')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch tweets for {account}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find tweet containers
    tweet_divs = soup.find_all("table", class_="tweet", limit=count)
    
    tweets = []
    for tweet in tweet_divs:
        text_div = tweet.find("div", class_="dir-ltr")
        if text_div:
            tweets.append(text_div.get_text(separator=" ").strip())

    return tweets

# Example accounts
accounts = ["@AP", "@Reuters", "@BBCBreaking"]

for account in accounts:
    print(f"\nTweets from {account}:")
    tweets = fetch_latest_tweets(account, count=5)
    for i, tweet in enumerate(tweets, 1):
        print(f"{i}. {tweet}")
