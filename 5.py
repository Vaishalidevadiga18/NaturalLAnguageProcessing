from collections import defaultdict

# Training data
train_data = [
    (["fun", "couple", "love", "love"], "comedy"),
    (["fast", "furious", "shoot"], "action"),
    (["couple", "fly", "fast", "fun", "fun"], "comedy"),
    (["furious", "shoot", "shoot", "fun"], "action"),
    (["fly", "fast", "shoot", "love"], "action")
]

# Document to classify
D = ["fast", "couple", "shoot", "fly"]

# Count documents and words
class_counts = defaultdict(int)
word_counts = defaultdict(lambda: defaultdict(int))
vocab = set()

# Build word and class frequency counts
for words, label in train_data:
    class_counts[label] += 1
    for word in words:
        word_counts[label][word] += 1
        vocab.add(word)

# Total number of documents
total_docs = sum(class_counts.values())
vocab_size = len(vocab)

# Compute total words per class
total_words_per_class = {
    label: sum(word_counts[label].values())
    for label in class_counts
}

# Compute actual probability using Naive Bayes with add-1 smoothing
def compute_prob(words, label):
    prior = class_counts[label] / total_docs
    likelihood = 1.0
    total_words = total_words_per_class[label]
    for word in words:
        # Add-1 smoothing
        count = word_counts[label][word]
        prob = (count + 1) / (total_words + vocab_size)
        likelihood *= prob
    return prior * likelihood

# Compute probabilities for each class
probs = {}
for label in class_counts:
    probs[label] = compute_prob(D, label)

# Normalize probabilities (optional, to compare as %)
total_prob = sum(probs.values())
normalized_probs = {label: prob / total_prob for label, prob in probs.items()}

# Predict the most probable class
predicted_class = max(probs, key=probs.get)

# Output results
print("Actual probabilities:", normalized_probs)
print("Predicted class:", predicted_class)
