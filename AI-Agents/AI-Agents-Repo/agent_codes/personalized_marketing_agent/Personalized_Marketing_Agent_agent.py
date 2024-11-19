
# Importing Required Libraries
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Personalized Marketing Agent Class
class PersonalizedMarketingAgent:
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=self.n_clusters)
        self.scaler = MinMaxScaler()

    def fit(self, data):
        self.data = data
        self.data_scaled = self.scaler.fit_transform(self.data)
        self.kmeans.fit(self.data_scaled)

    def recommend(self, customer_data):
        customer_data_scaled = self.scaler.transform([customer_data])
        label = self.kmeans.predict(customer_data_scaled)[0]
        recommendations = self.data[self.kmeans.labels_ == label]
        return recommendations.sample(5)  # Return 5 recommendations

# Hypothetical Data
data = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6],
    'age': [25, 35, 45, 55, 65, 75],
    'income': [50000, 60000, 70000, 80000, 90000, 100000],
    'purchased_items': ['item1', 'item2', 'item3', 'item4', 'item5', 'item6']
})

# Instantiate the Agent
agent = PersonalizedMarketingAgent()

# Fit the Data
agent.fit(data[['age', 'income']])

# Make a Recommendation
customer_data = [30, 55000]  # Hypothetical Customer Data
recommendations = agent.recommend(customer_data)

print("Recommendations for the customer: ", recommendations)
