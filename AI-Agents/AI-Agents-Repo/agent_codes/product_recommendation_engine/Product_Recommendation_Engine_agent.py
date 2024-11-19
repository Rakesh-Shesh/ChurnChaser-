
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

class ProductRecommendationEngine:
    def __init__(self, path):
        self.data = pd.read_csv(path)
        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)

    def train(self):
        pivot = self.data.pivot(index='productId', columns='userId', values='rating').fillna(0)
        matrix = csr_matrix(pivot.values)
        self.model_knn.fit(matrix)

    def recommend(self, product_id, num_recommendations=5):
        distances, indices = self.model_knn.kneighbors(self.data[self.data['productId'] == product_id].values.reshape(1, -1), n_neighbors = num_recommendations)
        return [self.data.iloc[i]['productId'] for i in indices.flatten()]

if __name__ == "__main__":
    path = 'path_to_your_data.csv'
    engine = ProductRecommendationEngine(path)
    engine.train()
    recommendations = engine.recommend('product_id', 5)
    print(recommendations)
