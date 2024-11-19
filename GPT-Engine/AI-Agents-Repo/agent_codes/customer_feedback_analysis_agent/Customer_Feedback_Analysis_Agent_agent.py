
# Importing required libraries
from textblob import TextBlob
import pandas as pd

class CustomerFeedbackAnalysisAgent:
    def __init__(self, feedback_data_path):
        self.data_path = feedback_data_path
        self.feedback_data = self.load_data()

    # Function to load customer feedback data
    def load_data(self):
        try:
            data = pd.read_csv(self.data_path)
            return data
        except Exception as e:
            return str(e)

    # Function to preprocess and clean text
    def preprocess_text(self, text):
        try:
            blob = TextBlob(text)
            return ' '.join(blob.words)
        except Exception as e:
            return str(e)

    # Function to get sentiment polarity
    def get_polarity(self, text):
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except Exception as e:
            return str(e)

    # Function to analyze customer feedback
    def analyze_feedback(self):
        try:
            # Preprocessing text
            self.feedback_data['clean_feedback'] = self.feedback_data['feedback'].apply(self.preprocess_text)

            # Getting sentiment polarity
            self.feedback_data['polarity'] = self.feedback_data['clean_feedback'].apply(self.get_polarity)

            # Classifying feedback as positive, negative and neutral
            self.feedback_data['sentiment'] = self.feedback_data['polarity'].apply(lambda polarity : 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral')

            return self.feedback_data
        except Exception as e:
            return str(e)

# Testing the CustomerFeedbackAnalysisAgent
if __name__ == "__main__":
    agent = CustomerFeedbackAnalysisAgent('path_to_customer_feedback_data.csv')
    analyzed_data = agent.analyze_feedback()
    print(analyzed_data)
