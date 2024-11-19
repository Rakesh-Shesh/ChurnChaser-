
# Required Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

class FraudDetectionAgent:
    def __init__(self, data_file):
        self.data_file = data_file
        self.model = LogisticRegression()

    def load_data(self):
        # Load data from a CSV file
        data = pd.read_csv(self.data_file)
        return data

    def preprocess_data(self, data):
        # Preprocessing steps like encoding, scaling, missing value treatment, etc.
        # For simplicity, it's assumed that data is already preprocessed
        return data

    def train(self, data):
        # Split data into training and testing sets
        X = data.drop('isFraud', axis=1)
        y = data['isFraud']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train)

        # Predict on the test data and calculate accuracy
        y_pred = self.model.predict(X_test)
        print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
        print(f'Confusion Matrix: \n{confusion_matrix(y_test, y_pred)}')

    def detect_fraud(self, new_data):
        # Predict if new data is fraud or not
        prediction = self.model.predict(new_data)
        return prediction


if __name__ == "__main__":
    agent = FraudDetectionAgent('data.csv')
    data = agent.load_data()
    processed_data = agent.preprocess_data(data)
    agent.train(processed_data)

    # new_data should be preprocessed in the same way as the training data
    new_data = pd.DataFrame()  # new data to predict
    print(agent.detect_fraud(new_data))
