# privacy_k_anonymity.py
import pandas as pd

df = pd.read_csv("output/sentiment_only.csv")

df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M')

agg_df = df.groupby(['Date', 'Sentiment']).size().reset_index(name='Count')
agg_df = agg_df[agg_df['Count'] >= 5]

agg_df.to_csv("output/k_anonymized_sentiment.csv", index=False)
print("✅ k-Anonymized sentiment data saved.")