from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity
import numpy as np
import pandas as pd
# Documents
documents = [
    "Shipment of gold damaged in a fire",
    "Delivery of silver arrived in a silver truck",
    "Shipment of gold arrived in a truck",
    "Purchased silver and gold arrived in a wooden truck",
    "The arrival of gold and silver shipment is delayed"
]
# Query
query = "gold silver truck"
# Combine all for vectorization
all_texts = documents + [query]
# Vectorize using term frequency
vectorizer = CountVectorizer(lowercase=True, stop_words='english')
X = vectorizer.fit_transform(all_texts).toarray()
# Separate query vector
doc_vectors = X[:-1]
query_vector = X[-1:]
# Compute distances/similarity
euclidean = euclidean_distances(doc_vectors, query_vector).flatten()
manhattan = manhattan_distances(doc_vectors, query_vector).flatten()
cosine = cosine_similarity(doc_vectors, query_vector).flatten()
# Prepare and sort results
results = pd.DataFrame({
    "Document": [f"D{i+1}" for i in range(len(documents))],
    "Euclidean": euclidean,
    "Manhattan": manhattan,
    "Cosine": cosine
})

# Sort and show top 2 for each metric
print("Top 2 Documents by Euclidean Distance (lowest is best):")
print(results.sort_values("Euclidean").head(2), '\n')
print("Top 2 Documents by Manhattan Distance (lowest is best):")
print(results.sort_values("Manhattan").head(2), '\n')
print("Top 2 Documents by Cosine Similarity (highest is best):")
print(results.sort_values("Cosine", ascending=False).head(2))

