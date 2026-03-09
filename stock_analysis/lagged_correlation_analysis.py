#correlation analysis with lagged data

import pandas as pd
from scipy.stats import pearsonr
import yfinance as yf

df_sent = pd.read_csv("output/sentiment_only.csv")
sentiment_map = {'POSITIVE': 1, 'NEUTRAL': 0, 'NEGATIVE': -1}
df_sent['Score'] = df_sent['Sentiment'].map(sentiment_map)
df_sent['Date'] = pd.to_datetime(df_sent['Date']).dt.date

df_sent = df_sent[['Date', 'Score']]

start_date = (pd.to_datetime(df_sent['Date'].min()) - pd.Timedelta(days=365)).strftime('%Y-%m-%d')
end_date = (pd.to_datetime(df_sent['Date'].max()) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

print(f"Fetching TSLA stock data from {start_date} to {end_date}...")
df_price = yf.download("TSLA", start=start_date, end=end_date)

df_price = df_price.reset_index()

df_price.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

df_price['Date'] = pd.to_datetime(df_price['Date']).dt.date

df_price = df_price[['Date', 'Close']]

stock_latest_date = df_price['Date'].max()
df_sent = df_sent[df_sent['Date'] <= stock_latest_date]

df_sentiment_daily = df_sent.groupby('Date').mean().reset_index()

df_merged = pd.merge(df_sentiment_daily, df_price, on='Date', how='inner')

print(f"Merged rows: {len(df_merged)}")

df_merged['Lagged_Score'] = df_merged['Score']

df_merged = df_merged.dropna()

if not df_merged.empty:
    corr, _ = pearsonr(df_merged['Lagged_Score'], df_merged['Close'])
    print(f"✅ Pearson Correlation (Same-Day Sentiment -> Close): {corr:.3f}")
else:
    print("⚠️ Not enough data to calculate correlation.")

df_merged.to_csv("output/merged_lagged_sentiment_stock.csv", index=False)
