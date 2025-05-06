import tweepy
import os

client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

response = client.get_tweet(
    id="1911929153244320237",
    tweet_fields=["public_metrics"]
)

print(response.data["public_metrics"])
