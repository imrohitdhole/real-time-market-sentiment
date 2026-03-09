# dashboard_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Stock Market Sentiment Analysis Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Sentiment Analysis System")

# Load all datasets
sentiment_df = pd.read_csv("output/sentiment_only.csv")
merged_df = pd.read_csv("output/merged_lagged_sentiment_stock.csv")
sentiment_anomalies = pd.read_csv("output/sentiment_anomalies.csv")
price_anomalies = pd.read_csv("output/price_anomalies.csv")
reservoir_sample = pd.read_csv("output/reservoir_sampled_sentiment.csv")
lsh_similar_pairs = pd.read_csv("output/lsh_similar_pairs.csv")
k_anonymized_sentiment = pd.read_csv("output/k_anonymized_sentiment.csv")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to:", ["📈 Overview", "🔍 Sentiment Trends", "📉 Anomaly Detection", "🧮 Reservoir Sampling", "🛡️ Privacy (k-Anonymity)", "🧩 Similar Phrases (LSH)"])

# 1. Overview
if selection == "📈 Overview":
    st.header("🔹 System Overview")
    st.markdown("""
    Welcome to the Real-Time Stock Market Sentiment Analysis Dashboard.
    
    **Main Features**:
    - Real-time news ingestion with Kafka
    - Real-time sentiment analysis with Spark
    - Correlation with Stock Prices
    - Anomaly Detection (Sentiment and Stock)
    - Privacy (k-Anonymity)
    - Approximate Similar Phrase Detection (LSH)
    """)
    st.subheader("📋 Key Datasets Summary:")
    st.dataframe({
        "Dataset": ["Sentiment Only", "Merged Sentiment-Stock", "Sentiment Anomalies", "Price Anomalies", "Reservoir Sample", "LSH Similar Pairs", "k-Anonymized Sentiment"],
        "Rows": [len(sentiment_df), len(merged_df), len(sentiment_anomalies), len(price_anomalies), len(reservoir_sample), len(lsh_similar_pairs), len(k_anonymized_sentiment)]
    })

# 2. Sentiment Trends
elif selection == "🔍 Sentiment Trends":
    st.header("🔹 Sentiment Trend vs Stock Close Price")
    
    merged_df['Date'] = pd.to_datetime(merged_df['Date'])
    
    fig1 = px.line(merged_df, x='Date', y='Lagged_Score', title="Sentiment Trend Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(merged_df, x='Date', y='Close', title="Stock Close Price Over Time")
    st.plotly_chart(fig2, use_container_width=True)

# 3. Anomaly Detection
elif selection == "📉 Anomaly Detection":
    st.header("🔹 Anomaly Detection in Sentiment and Prices")
    
    sentiment_anomalies['Date'] = pd.to_datetime(sentiment_anomalies['Date'])
    price_anomalies['Date'] = pd.to_datetime(price_anomalies['Date'])

    st.subheader("Sentiment Anomalies")
    fig3 = px.scatter(sentiment_anomalies, x="Date", y="Lagged_Score", color_discrete_sequence=["red"], title="Sentiment Anomalies")
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(sentiment_anomalies)

    st.subheader("Price Anomalies")
    fig4 = px.scatter(price_anomalies, x="Date", y="Close", color_discrete_sequence=["purple"], title="Price Anomalies")
    st.plotly_chart(fig4, use_container_width=True)
    st.dataframe(price_anomalies)

# 4. Reservoir Sampling
elif selection == "🧮 Reservoir Sampling":
    st.header("🔹 Random Reservoir Sampling of Sentiments")
    st.dataframe(reservoir_sample)

# 5. Privacy K-Anonymity
elif selection == "🛡️ Privacy (k-Anonymity)":
    st.header("🔹 Privacy-Preserved Sentiment Dataset (k-Anonymity Applied)")
    st.dataframe(k_anonymized_sentiment)

# 6. Similar Phrases (LSH)
elif selection == "🧩 Similar Phrases (LSH)":
    st.header("🔹 Detected Highly Similar Financial Phrases (via LSH)")
    st.dataframe(lsh_similar_pairs)

