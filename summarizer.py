#import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

'''
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
'''

import google.generativeai as genai

# Summarize using Google Gemini
def summarize_text(text):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = f"Summarize the following article in 1 paragraph that is 4-5 sentences, keeping the core information and neutral tone, with no bias:\n\n{text}\n\nSummary:"
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


from news_fetcher import get_articles

# Get summaries for all articles
def get_article_summaries(category='general'):
    articles, urls = get_articles(category)
    summaries = {}
    for title, content in articles.items():
        summaries[title] = summarize_text(content)
    return summaries, urls

'''
# Post back to Twitter
def post_summary(summary, source_account):
    formatted = f"📢 Summary of @{source_account}'s latest post:\n\n{summary}\n\n#news #AIagent"
    api.update_status(formatted)
'''

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
