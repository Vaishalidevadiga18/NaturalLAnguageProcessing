from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity
import pandas as pd
# Documents
documents = [
    "Shipment of gold damaged in a fire",
    "Delivery of silver arrived in a silver truck",
    "Shipment of gold arrived in a truck",
    "Shipment of gold and silver arrived in a truck",
    "The arrival of gold and silver shipments is delayed"
]
# Query
query = ["gold silver truck"]
# Vectorize using CountVectorizer (TF)
vectorizer = CountVectorizer()
doc_vectors = vectorizer.fit_transform(documents + query).toarray()
# Separate query vector
query_vector = doc_vectors[-1]
doc_vectors = doc_vectors[:-1]
# Compute similarity/distance scores
euclidean = euclidean_distances(doc_vectors, [query_vector]).flatten()
manhattan = manhattan_distances(doc_vectors, [query_vector]).flatten()
cosine = cosine_similarity(doc_vectors, [query_vector]).flatten()
# Create DataFrame with scores
results = pd.DataFrame({
    "Document": documents,
    "Euclidean Distance": euclidean,
    "Manhattan Distance": manhattan,
    "Cosine Similarity": cosine
})
# Sort and display most similar documents
print("Top documents by Cosine Similarity:")
print(results.sort_values(by="Cosine Similarity", ascending=False)[["Document", "Cosine Similarity"]], end="\n\n")
print("Top documents by Euclidean Distance:")
print(results.sort_values(by="Euclidean Distance")[["Document", "Euclidean Distance"]], end="\n\n")
print("Top documents by Manhattan Distance:")
print(results.sort_values(by="Manhattan Distance")[["Document", "Manhattan Distance"]])
print("Top 2 Documents by Euclidean Distance (lowest is best):")
print(results.sort_values("Euclidean Distance").head(2), '\n')
print("Top 2 Documents by Manhattan Distance (lowest is best):")
print(results.sort_values("Manhattan Distance").head(2), '\n')
print("Top 2 Documents by Cosine Similarity (highest is best):")
print(results.sort_values("Cosine Similarity", ascending=False).head(2))

# Sort by Euclidean Distance and display top 2 most similar documents
top2_euclidean = results.sort_values(by="Euclidean Distance").head(2)
print("Top 2 most similar documents based on Euclidean Distance:")
for i, row in top2_euclidean.iterrows():
    print(f"{i+1}. {row['Document']} (Distance: {row['Euclidean Distance']:.4f})")
top2_MANH = results.sort_values(by="Manhattan Distance").head(2)
print("\nTop 2 most similar documents based on Manhattan Distance:")
for i, row in top2_MANH.iterrows():
    print(f"{i+1}. {row['Document']} (Distance: {row['Manhattan Distance']:.4f})")
top2_cosine = results.sort_values(by="Cosine Similarity").head(2)
print("\nTop 2 most similar documents based on Cosine similarity:")
for i, row in top2_cosine.iterrows():
    print(f"{i+1}. {row['Document']} (Distance: {row['Cosine Similarity']:.4f})")
