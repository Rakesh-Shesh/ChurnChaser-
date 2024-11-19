
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

class SalesLeadScoringAgent:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.X = self.data.iloc[:, :-1].values
        self.y = self.data.iloc[:, -1].values
        self.classifier = None

    def preprocess_data(self):
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=0)
        
        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        
        return X_train, X_test, y_train, y_test

    def train(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        
        # Train the model
        self.classifier = RandomForestClassifier(n_estimators=20, random_state=0)
        self.classifier.fit(X_train, y_train)

        # Make predictions
        y_pred = self.classifier.predict(X_test)

        # Evaluate the model
        cm = confusion_matrix(y_test, y_pred)
        print('Confusion Matrix: ', cm)
        print('Accuracy: ', accuracy_score(y_test, y_pred))

    def score_lead(self, lead_features):
        if not self.classifier:
            print('Model not trained yet.')
            return None

        lead = [lead_features]
        score = self.classifier.predict(lead)
        return score

if __name__ == "__main__":
    agent = SalesLeadScoringAgent('data.csv')
    agent.train()

    # Score a lead
    lead_features = [2.5, 3.0, 4.5, 5.0]  # replace with actual features
    print('Lead Score: ', agent.score_lead(lead_features))
