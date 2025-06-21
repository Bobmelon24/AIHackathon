import tweepy, os
from dotenv import load_dotenv

load_dotenv()

# Tweepy Authentication
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_SECRET_API_KEY"),
    os.getenv("TWITTER_CLIENT_ID"),
    os.getenv("TWITTER_CLIENT_SECRET")
)
api = tweepy.API(auth)

accounts = ["@AP", "@Reuters", "@BBCBreaking"]

# Fetch Recent Tweets
def fetch_latest_tweets(account, count=5):
    tweets = api.user_timeline(screen_name=account, count=count, tweet_mode="extended", exclude_replies=True)
    return [t.full_text for t in tweets if not t.full_text.startswith("RT")]


# Summarize using Google Gemini
def summarize_text(text):
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"Summarize the following tweet in 1–2 sentences, keeping the core news and neutral tone:\n\n{text}\n\nSummary:"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()


# Post back to Twitter
def post_summary(summary, source_account):
    formatted = f"📢 Summary of @{source_account}'s latest post:\n\n{summary}\n\n#news #AIagent"
    api.update_status(formatted)

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

