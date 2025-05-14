import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


class SemanticMappingSketch:
    def __init__(self, embeddings_dict, bins_per_dim=4, pca_dim=4):
        self.bins_per_dim = bins_per_dim
        self.pca_dim = pca_dim

        # Load and reduce dimensionality
        self.words = list(embeddings_dict.keys())
        X = np.array([embeddings_dict[w] for w in self.words])

        self.pca = PCA(n_components=pca_dim)
        reduced = self.pca.fit_transform(X)

        self.scaler = MinMaxScaler()
        self.normalized = self.scaler.fit_transform(reduced)

        # Map words to cells
        self.word_to_cell = {
            word: self.vector_to_cell(vec)
            for word, vec in zip(self.words, self.normalized)
        }

        # Initialize sketch structure (cell → count)
        self.sketch = {}

    def vector_to_cell(self, vector):
        coords = tuple((vector * self.bins_per_dim).astype(int).clip(0, self.bins_per_dim - 1))
        return coords

    def insert(self, word, count=1):
        if word not in self.word_to_cell:
            return
        cell = self.word_to_cell[word]
        self.sketch[cell] = self.sketch.get(cell, 0) + count

    def estimate(self, word):
        if word not in self.word_to_cell:
            return 0
        cell = self.word_to_cell[word]
        return self.sketch.get(cell, 0)


import gensim.downloader as api

api.info()
# Load pre-trained embeddings
model = api.load("glove-wiki-gigaword-100")

# Convert to dict
embeddings_dict = {word: model[word] for word in ["dog", "wolf", "car", "apple", "banana", "truck", "cat"] if word in model}

# Create sketch
sms = SemanticMappingSketch(embeddings_dict)

# Insert some words
sms.insert("dog", 5)
sms.insert("wolf", 3)
sms.insert("car", 1)

# Estimate frequencies
print("dog:", sms.estimate("dog"))  # shares cell with "wolf" if similar
print("wolf:", sms.estimate("wolf"))
print("apple:", sms.estimate("apple"))
