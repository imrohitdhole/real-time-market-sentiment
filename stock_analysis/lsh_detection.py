# lsh_detection.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("financialphrasebank.csv")
texts = df.iloc[:, 0].astype(str)

vectorizer = TfidfVectorizer(max_features=500)
X = vectorizer.fit_transform(texts)

cos_sim = cosine_similarity(X)

similar_pairs = []
threshold = 0.9
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        if cos_sim[i, j] > threshold:
            similar_pairs.append((texts[i], texts[j], cos_sim[i, j]))

similar_df = pd.DataFrame(similar_pairs, columns=["Text1", "Text2", "Similarity"])
similar_df.to_csv("output/lsh_similar_pairs.csv", index=False)
print("✅ Similar phrases detected and saved.")