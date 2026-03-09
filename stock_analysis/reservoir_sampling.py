# reservoir_sampling.py
import pandas as pd
import random

df = pd.read_csv("output/sentiment_only.csv")

sample_size = 100
reservoir = []

for i, row in enumerate(df.itertuples(index=False)):
    if i < sample_size:
        reservoir.append(row)
    else:
        j = random.randint(0, i)
        if j < sample_size:
            reservoir[j] = row

sampled_df = pd.DataFrame(reservoir)
sampled_df.columns = df.columns
sampled_df.to_csv("output/reservoir_sampled_sentiment.csv", index=False)
print("✅ Reservoir Sampling completed. Sampled data saved.")