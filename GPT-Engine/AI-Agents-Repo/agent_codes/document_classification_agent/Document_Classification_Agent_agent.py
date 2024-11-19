
# Importing necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd

class DocumentClassificationAgent:
    def __init__(self):
        self.classifier = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),
        ])

    def train(self, documents, labels):
        docs_train, docs_test, labels_train, labels_test = train_test_split(documents, labels, test_size=0.2)
        self.classifier.fit(docs_train, labels_train)
        predicted = self.classifier.predict(docs_test)
        print("Accuracy:", (predicted == labels_test).mean())

    def classify(self, new_document):
        return self.classifier.predict([new_document])

# Assuming you have a CSV file with two columns: "text" for the document content and "label" for its category
df = pd.read_csv('documents.csv')

agent = DocumentClassificationAgent()
agent.train(df['text'], df['label'])

# Testing the agent with a new document
print(agent.classify('This is a new document.'))
