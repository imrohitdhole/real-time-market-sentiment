#stock_sentiment.py
import pandas as pd
import json
from kafka import KafkaConsumer
from datetime import datetime

consumer = KafkaConsumer(
    'sentimentdata',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    consumer_timeout_ms=10000, 
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

data = []
try:
    for msg in consumer:
        val = msg.value
        if 'publishedAt' in val and 'sentiment' in val:
            date = datetime.strptime(val['publishedAt'][:10], '%Y-%m-%d').date()
            data.append((date, val['sentiment']))
except Exception as e:
    print("⚠️ Kafka consumption error:", e)

if data:
    df = pd.DataFrame(data, columns=['Date', 'Sentiment'])
    df.to_csv("output/sentiment_only.csv", index=False)
    print(f"✅ Saved sentiment_only.csv with {len(data)} records")
else:
    print("⚠️ No sentiment data received from Kafka.")
