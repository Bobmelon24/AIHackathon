import tweepy
import os
import time

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

# Initialize Tweepy client using bearer token
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Cache usernames to user IDs to avoid rate limits on get_user
USER_ID_CACHE = {}

def fetch_latest_tweets(account_username, count=5):
    try:
        # Use cache to avoid calling get_user too often
        if account_username not in USER_ID_CACHE:
            user = client.get_user(username=account_username)
            USER_ID_CACHE[account_username] = user.data.id
            time.sleep(1)  # minor delay to reduce pressure

        user_id = USER_ID_CACHE[account_username]

        # Get tweets from user timeline
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=count,
            exclude=["retweets", "replies"],
            tweet_fields=["text"]
        )

        if not tweets.data:
            return []

        return [tweet.text for tweet in tweets.data]

    except TooManyRequests as e:
        reset_time = int(e.response.headers.get("x-rate-limit-reset", time.time() + 60))
        wait_time = max(0, reset_time - int(time.time()))
        print(f"🚫 Rate limit hit. Waiting {wait_time} seconds...")
        time.sleep(wait_time + 1)
        return fetch_latest_tweets(account_username, count)  # retry after wait

    except Exception as e:
        print(f"Error fetching tweets for @{account_username}: {e}")
        return []

# Test function
def test_fetch_latest_tweets():
    accounts = ["AP", "BBCBreaking", "CNN"]  # You can test multiple accounts here
    for account in accounts:
        print(f"\nFetching tweets for @{account}...")
        tweets = fetch_latest_tweets(account, count = 5)  # valid range is 5–100)
        for i, tweet in enumerate(tweets, 1):
            print(f"\nTweet {i}:\n{tweet}")
        time.sleep(2)  # Throttle between accounts

if __name__ == "__main__":
    test_fetch_latest_tweets()



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
