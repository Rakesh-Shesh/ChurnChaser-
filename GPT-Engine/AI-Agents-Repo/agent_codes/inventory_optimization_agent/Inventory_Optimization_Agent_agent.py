
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Define the inventory optimization agent
class InventoryOptimizationAgent:
    def __init__(self, inventory_df):
        self.inventory_df = inventory_df
        self.model = LinearRegression()

    def preprocess_data(self):
        # Split data into features (X) and target (y)
        X = self.inventory_df.drop('demand', axis=1)
        y = self.inventory_df['demand']

        # Split data into training and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        # Train the model
        self.model.fit(self.X_train, self.y_train)

    def predict_demand(self):
        # Use the model to predict demand
        self.predictions = self.model.predict(self.X_test)

    def optimize_inventory(self):
        # Calculate optimal inventory level for each product
        self.optimized_inventory = self.predictions + self.X_test['supply']
        return self.optimized_inventory

    def run_agent(self):
        self.preprocess_data()
        self.train_model()
        self.predict_demand()
        return self.optimize_inventory()

# Create a dataframe for the inventory
# For simplicity, let's assume we have only two features: product_id and supply, and one target: demand
inventory_df = pd.DataFrame({
    'product_id': [1, 2, 3, 4, 5],
    'supply': [100, 200, 150, 300, 250],
    'demand': [110, 210, 160, 310, 260]
})

# Create an instance of the agent and run it
agent = InventoryOptimizationAgent(inventory_df)
optimized_inventory = agent.run_agent()
print(optimized_inventory)
