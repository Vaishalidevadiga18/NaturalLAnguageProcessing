import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from sklearn.preprocessing import Binarizer
# Step 1: Documents and query
documents = [
    "It is going to rain today",
    "Today Rama is not going outside to watch rain",
    "I am going to watch the movie tomorrow with Rama",
    "Tomorrow Rama is going to watch the rain at sea shore"
]
query = "Rama watching the rain"
# Step 2: TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X_tfidf = vectorizer.fit_transform(documents + [query])
# Step 3: Apply Truncated SVD (LSA)
svd = TruncatedSVD(n_components=2)  # 2D latent space
X_lsa = svd.fit_transform(X_tfidf)
doc_vectors = X_lsa[:-1]
query_vector = X_lsa[-1:]
euclidean = euclidean_distances(doc_vectors, query_vector).flatten()
cosine = cosine_similarity(doc_vectors, query_vector).flatten()
X_binary = Binarizer().fit_transform(X_tfidf.toarray())
doc_bin = X_binary[:-1]
query_bin = X_binary[-1:]
def jaccard(a, b):
    return np.sum(np.minimum(a, b)) / np.sum(np.maximum(a, b))
def dice(a, b):
    return 2 * np.sum(np.minimum(a, b)) / (np.sum(a) + np.sum(b))
jaccard_scores = [jaccard(doc, query_bin) for doc in doc_bin]
dice_scores = [dice(doc, query_bin) for doc in doc_bin]
df = pd.DataFrame({
    "Document": [f"D{i+1}" for i in range(len(documents))],
    "Euclidean Distance": euclidean,
    "Cosine Similarity": cosine,
    "Jaccard Similarity": jaccard_scores,
    "Dice Similarity": dice_scores
})
df["Inverse Euclidean"] = 1 / (1 + df["Euclidean Distance"])
df.set_index("Document")[["Inverse Euclidean", "Cosine Similarity", "Jaccard Similarity", "Dice Similarity"]].plot(
    kind='bar', figsize=(10, 6), colormap='viridis')
plt.title("Similarity Measures to Query: 'Rama watching the rain'")
plt.ylabel("Similarity Score (Higher is Better)")
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
print(df.sort_values(by="Cosine Similarity", ascending=False).head(2))
