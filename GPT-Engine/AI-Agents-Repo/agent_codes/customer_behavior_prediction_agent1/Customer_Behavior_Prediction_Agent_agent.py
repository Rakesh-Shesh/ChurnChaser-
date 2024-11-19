import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine
import joblib
import os
import requests
from shap import TreeExplainer
import shap

# Load data
data = pd.read_csv('customer_data.csv')

# Clean and preprocess data
data = data.drop('CustomerID', axis=1)
data = pd.get_dummies(data)  # One-hot encoding for categorical variables

# Split data into features (X) and target (y)
X = data.drop('Behavior', axis=1)
y = data['Behavior']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
predictions = model.predict(X_test)

# Evaluate the model
print("Model Accuracy: ", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

# Save the model to disk for future predictions
joblib.dump(model, 'customer_behavior_model.pkl')

# Connect to a database (PostgreSQL example)
db_engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')


# Store model evaluation results into a database
def store_model_performance():
    accuracy = accuracy_score(y_test, predictions)
    performance_df = pd.DataFrame({'accuracy': [accuracy], 'report': [classification_report(y_test, predictions)]})
    performance_df.to_sql('model_performance', db_engine, if_exists='replace', index=False)


store_model_performance()


# Email integration function
def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


# Send a notification email when a high-potential customer is identified
def notify_high_potential_customer(customer_id):
    email_subject = f"High Potential Customer Identified: {customer_id}"
    email_body = f"The customer with ID {customer_id} has been identified as a high potential customer."
    send_email(email_subject, email_body, "marketing_team@example.com")


# Predict function using the model
class CustomerBehaviorPredictionAgent:
    def __init__(self, model):
        self.model = model

    def predict(self, customer_data):
        customer_data = pd.get_dummies(customer_data)
        prediction = self.model.predict(customer_data)

        # Notify if the customer is high potential (prediction = 1)
        if prediction[0] == 1:
            notify_high_potential_customer(customer_data['CustomerID'].values[0])

        return prediction


# Example: Predict for a new customer
new_customer_data = pd.DataFrame({
    'Age': [35],
    'Annual_Income': [50000],
    'Previous_Purchases': [10],
    'Behavior': [0]
})
agent = CustomerBehaviorPredictionAgent(model)
predicted_behavior = agent.predict(new_customer_data)
print("Predicted Behavior:", predicted_behavior)


# Periodic Retraining (optional - can be scheduled with a cron job)
def retrain_model():
    new_data = pd.read_csv('new_customer_data.csv')  # Assume new data is available
    X_new = new_data.drop('Behavior', axis=1)
    y_new = new_data['Behavior']

    X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(X_new, y_new, test_size=0.2, random_state=42)
    new_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    new_model.fit(X_train_new, y_train_new)

    # Save the updated model
    joblib.dump(new_model, 'customer_behavior_model.pkl')


# Model Interpretation (using SHAP)
def explain_model():
    explainer = TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # Visualize the SHAP values
    shap.summary_plot(shap_values[1], X)  # Focus on the positive class (Behavior = 1)


# Call the function to explain the model
explain_model()

