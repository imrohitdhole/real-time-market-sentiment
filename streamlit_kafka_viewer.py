import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd

st.title("📈 Real-Time Sentiment Stream (Kafka Topic: sentimentdata)")

# Set up Kafka Consumer
consumer = KafkaConsumer(
    'sentimentdata',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    consumer_timeout_ms=10000  # Stop after 10 sec if no new data
)

# Streamlit live updating
placeholder = st.empty()

messages = []
for message in consumer:
    msg = message.value
    messages.append(msg)

# Show all messages nicely
if messages:
    df = pd.DataFrame(messages)
    st.dataframe(df)
else:
    st.warning("⚠️ No data received from Kafka yet. Check if producers and spark jobs are running.")

st.success("✅ Stream ended. Rerun to refresh latest messages.")
