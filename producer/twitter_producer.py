import os
import json
import tweepy
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

query = "stock OR market lang:en -is:retweet"
tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["created_at"])

for tweet in tweets.data:
    msg = {
        "text": tweet.text,
        "created_at": tweet.created_at.strftime("%Y-%m-%dT%H:%M:%S")
    }
    producer.send("twitterdata", msg)
    print("Tweet sent:", msg["text"])
