# anomaly_detection.py 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("output/merged_lagged_sentiment_stock.csv")

sentiment_mean = df['Lagged_Score'].mean()
sentiment_std = df['Lagged_Score'].std()
df['Sentiment_Zscore'] = (df['Lagged_Score'] - sentiment_mean) / sentiment_std

price_mean = df['Close'].mean()
price_std = df['Close'].std()
df['Price_Zscore'] = (df['Close'] - price_mean) / price_std

threshold = 2.0

sentiment_anomalies = df[np.abs(df['Sentiment_Zscore']) > threshold]
price_anomalies = df[np.abs(df['Price_Zscore']) > threshold]

print("✅ Detected Sentiment Anomalies:", len(sentiment_anomalies))
print("✅ Detected Price Anomalies:", len(price_anomalies))

sentiment_anomalies.to_csv("output/sentiment_anomalies.csv", index=False)
price_anomalies.to_csv("output/price_anomalies.csv", index=False)