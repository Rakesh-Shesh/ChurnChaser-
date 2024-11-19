import nltk
from nltk.corpus import stopwords
from profanity_check import predict
from textblob import TextBlob
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging
import os
import time

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')


class ContentModerationAgent:
    def __init__(self, db_name="moderation_logs.db", email_config=None):
        self.stop_words = set(stopwords.words('english'))
        self.db_name = db_name
        self.email_config = email_config
        self.create_db()

    def create_db(self):
        """Create database to log moderated content."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS moderation_logs (
                id INTEGER PRIMARY KEY,
                content TEXT,
                profanity_detected BOOLEAN,
                sentiment TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def store_log(self, content, profanity_detected, sentiment):
        """Store content moderation log in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO moderation_logs (content, profanity_detected, sentiment)
            VALUES (?, ?, ?)
        """, (content, profanity_detected, sentiment))
        conn.commit()
        conn.close()

    def send_email_alert(self, content):
        """Send email alert when profanity is detected."""
        if not self.email_config:
            raise ValueError("Email configuration not set.")

        msg = MIMEMultipart()
        msg['From'] = self.email_config['from_email']
        msg['To'] = self.email_config['to_email']
        msg['Subject'] = 'Profanity Alert Detected'

        body = f"The following content was flagged for profanity:\n\n{content}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.email_config['from_email'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['from_email'], self.email_config['to_email'], text)

    def tokenize(self, text):
        """Tokenize text."""
        tokens = nltk.word_tokenize(text)
        return tokens

    def remove_stopwords(self, tokens):
        """Remove stopwords from tokenized text."""
        return [token for token in tokens if token.lower() not in self.stop_words]

    def check_profanity(self, text):
        """Check if the text contains profanity."""
        if predict([text]):
            return True
        return False

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the text."""
        blob = TextBlob(text)
        sentiment = "positive" if blob.sentiment.polarity > 0 else "negative" if blob.sentiment.polarity < 0 else "neutral"
        return sentiment

    def moderate_content(self, text):
        """Moderate the content based on profanity and sentiment."""
        # Tokenization and stop word removal
        tokens = self.tokenize(text)
        filtered_tokens = self.remove_stopwords(tokens)
        filtered_text = ' '.join(filtered_tokens)

        # Profanity check
        profanity_detected = self.check_profanity(text)

        # Sentiment analysis
        sentiment = self.analyze_sentiment(text)

        # Log content to DB
        self.store_log(text, profanity_detected, sentiment)

        # Send email if profanity is detected
        if profanity_detected and self.email_config:
            self.send_email_alert(text)

        # Return results
        return {
            'filtered_text': filtered_text,
            'profanity_detected': profanity_detected,
            'sentiment': sentiment
        }


def main():
    # Sample email configuration (use your own credentials here)
    email_config = {
        'from_email': 'youremail@gmail.com',
        'to_email': 'admin@example.com',
        'password': 'yourpassword'  # Use an app-specific password for Gmail if 2FA is enabled
    }

    agent = ContentModerationAgent(email_config=email_config)

    text = input("Enter the text to moderate: ")

    # Moderate the text
    result = agent.moderate_content(text)

    print(f"Filtered Text: {result['filtered_text']}")
    print(f"Profanity Detected: {result['profanity_detected']}")
    print(f"Sentiment: {result['sentiment']}")


if __name__ == "__main__":
    main()
