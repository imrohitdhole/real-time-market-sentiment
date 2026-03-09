# news_producer.py

# import requests
# import json
# import time
# import os
# import random
# from kafka import KafkaProducer
# from dotenv import load_dotenv
# import datetime

# load_dotenv()
# API_KEY = os.getenv("NEWS_API_KEY")
# producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# # Keywords to search for
# keywords = ["stocks", "Tesla", "Apple", "finance", "investment", "market"]

# while True:
#     today = datetime.date.today()
#     from_date = (today - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

#     for keyword in keywords:
#         url = f'https://newsapi.org/v2/everything?q={keyword}&from={from_date}&sortBy=publishedAt&pageSize=100&apiKey={API_KEY}'
#         response = requests.get(url)
#         if response.status_code == 200:
#             articles = response.json().get("articles", [])
#             for article in articles:
#                 # 🌟 Randomly assign a fake publishedAt date in the last 30 days
#                 random_days_back = random.randint(0, 365)
#                 fake_date = (today - datetime.timedelta(days=random_days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')

#                 msg = {
#                     "title": article.get("title"),
#                     "content": article.get("content") or "",
#                     "publishedAt": fake_date
#                 }
#                 producer.send("newsdata", msg)
#                 print(f"Sent ({keyword}):", msg["title"], "| Fake Date:", fake_date)
#         else:
#             print(f"Failed to fetch for {keyword}: {response.status_code}")

#     time.sleep(30)  # Fetch every 30 seconds

# news_producer.py (Offline Kaggle Dataset Version)

import pandas as pd
import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv("financialphrasebank.csv") 

title_templates = [
    "Market Insight: {}",
    "Stock Update: {}",
    "Finance News: {}",
    "Investor Alert: {}",
    "Trending Now: {}",
    "Breaking: {}",
    "Hot Stocks: {}",
    "Financial Brief: {}",
]

print("Loaded offline dataset with", len(df), "records")

while True:
    sampled = df.sample(50)  
    for _, row in sampled.iterrows():
        phrase = str(row.iloc[0])  
        random_title = random.choice(title_templates).format(phrase[:40])
        random_days_back = random.randint(0, 90)
        fake_date = (pd.Timestamp.today() - pd.Timedelta(days=random_days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')

        msg = {
            "title": random_title,
            "content": phrase,
            "publishedAt": fake_date
        }
        producer.send("offlinenewsdata", msg)
        print(f"Sent offline news:", msg["title"], "| Published At:", msg["publishedAt"])
    
    time.sleep(10)  
