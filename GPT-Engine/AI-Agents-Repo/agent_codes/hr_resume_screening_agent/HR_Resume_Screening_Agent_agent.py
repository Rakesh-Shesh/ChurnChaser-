
# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

class HrResumeScreeningAgent:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
        self.clf = MultinomialNB()
        
    def train(self, df):
        # split dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(df['resume'], df['class'], random_state = 0)
        
        # Convert text data into term frequency-inverse document frequency (tf-idf) format
        tfidf_train = self.vectorizer.fit_transform(X_train)
        tfidf_test = self.vectorizer.transform(X_test)
        
        # Train the Naive Bayes Classifier
        self.clf.fit(tfidf_train, y_train)
        
        # Predict the labels
        y_pred = self.clf.predict(tfidf_test)
        
        # Calculate accuracy
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print('Accuracy: ', accuracy)
        
    def predict(self, new_resume):
        # Convert text data into term frequency-inverse document frequency (tf-idf) format
        new_resume_tfidf = self.vectorizer.transform([new_resume])
        
        # Predict the label
        pred_label = self.clf.predict(new_resume_tfidf)
        
        return pred_label

df = pd.read_csv('resume_data.csv')  # assuming you have a csv file named 'resume_data.csv' with 'resume' and 'class' columns
agent = HrResumeScreeningAgent()
agent.train(df)

new_resume = "Here is a new resume..."  
print(agent.predict(new_resume))
