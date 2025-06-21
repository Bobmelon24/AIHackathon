import tweepy
import os
import time
import csv

from datetime import datetime
from tweepy.errors import TooManyRequests
from dotenv import load_dotenv

load_dotenv()

# Tweepy Authentication
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_SECRET_API_KEY"),
    os.getenv("TWITTER_ACCESS_KEY"),
    os.getenv("TWITTER_ACCESS_SECRET_KEY")
)
api = tweepy.API(auth)

accounts = ["@AP", "@Reuters", "@BBCBreaking"]
# Get the bearer token from env
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Username to user ID cache
USER_ID_CACHE = {}

def fetch_latest_tweets(account_username, count=5):
    try:
        count = max(5, min(100, count))

        if account_username not in USER_ID_CACHE:
            user = client.get_user(username=account_username)
            USER_ID_CACHE[account_username] = user.data.id
            time.sleep(1)

        user_id = USER_ID_CACHE[account_username]

        tweets = client.get_users_tweets(
            id=user_id,
            max_results=count,
            exclude=["retweets", "replies"],
            tweet_fields=["text", "created_at"]
        )

        if not tweets.data:
            return []

        return [
            {
                "timestamp": tweet.created_at.isoformat(),
                "account": account_username,
                "text": tweet.text.replace("\n", " ").strip()
            }
            for tweet in tweets.data
        ]

    except TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + 60))
        wait_time = max(0, reset_time - int(time.time()))
        print(f"Rate limit hit. Waiting {wait_time} seconds...")
        time.sleep(wait_time + 1)
        return fetch_latest_tweets(account_username, count)

    except BadRequest as e:
        print(f"Bad request for @{account_username}: {e}")
        return []

    except Exception as e:
        print(f"Error fetching tweets for @{account_username}: {e}")
        return []

def write_tweets_to_csv(tweets, filename="tweets.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "account", "text"])
        if not file_exists:
            writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)

def run_scraper():
    accounts = ["AP", "BBCBreaking", "CNN"]
    all_tweets = []
    for account in accounts:
        print(f"\nFetching tweets for @{account}...")
        tweets = fetch_latest_tweets(account, count=5)
        all_tweets.extend(tweets)
        time.sleep(2)
    write_tweets_to_csv(all_tweets)
    print(f"✅ Stored {len(all_tweets)} tweets at {datetime.utcnow().isoformat()} UTC.")
'''
if __name__ == "__main__":
    while True:
        run_scraper()
        print("⏳ Waiting 16 minutes before next run...\n")
        time.sleep(16 * 60)  # wait 960 seconds (16 minutes)
'''


# Summarize using Google Gemini
def summarize_text(text):
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"Summarize the following tweet in 1–2 sentences, keeping the core information and neutral tone, with no bias:\n\n{text}\n\nSummary:"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


# Post back to Twitter
def post_summary(summary, source_account):
    formatted = f"📢 Summary of @{source_account}'s latest post:\n\n{summary}\n\n#news #AIagent"
    api.update_status(formatted)

# Test Fetching Tweets
def test_fetch_latest_tweets():
    for account in accounts:
        print(f"Fetching tweets for {account}...")
        tweets = fetch_latest_tweets(account, count=1)
        print(f"Latest tweets from {account}:")
        for tweet in tweets:
            print(f"- {tweet}")

'''
# Automation Loop
import schedule, time

def summarize_and_post():
    for account in accounts:
        tweets = fetch_latest_tweets(account, count=3)
        for tweet in tweets:
            summary = summarize_text(tweet)
            post_summary(summary, account.strip("@"))
            time.sleep(10)  # Avoid rate limits

schedule.every(30).minutes.do(summarize_and_post)

while True:
    schedule.run_pending()
    time.sleep(1)
'''
