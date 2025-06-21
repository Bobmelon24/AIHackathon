import tweepy, os
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_SECRET_API_KEY"),
    os.getenv("TWITTER_CLIENT_ID"),
    os.getenv("TWITTER_CLIENT_SECRET")
)
api = tweepy.API(auth)
