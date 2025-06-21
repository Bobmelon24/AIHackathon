import tweepy, os
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuth1UserHandler(
    os.getenv("API_KEY"),
    os.getenv("SECRET_API_KEY"),
    os.getenv("CLIEND_ID"),
    os.getenv("CLIENT_SECRET")
)
api = tweepy.API(auth)
