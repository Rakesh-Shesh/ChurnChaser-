import tweepy
from textblob import TextBlob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import datetime

# Twitter API credentials (You should replace these with your own)
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Outlook Email credentials (You should replace these with your own)
outlook_email = 'your_outlook_email@example.com'
outlook_password = 'your_outlook_password'
recipient_email = 'recipient@example.com'


class BrandMonitoringAgent:
    def __init__(self, brand_name):
        self.brand_name = brand_name

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Create API object
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

    def get_brand_tweets(self, num_tweets):
        tweets = tweepy.Cursor(self.api.search,
                               q=self.brand_name,
                               lang="en").items(num_tweets)
        return tweets

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'

    def monitor(self, num_tweets):
        tweet_data = []
        tweets = self.get_brand_tweets(num_tweets)

        for tweet in tweets:
            sentiment = self.analyze_sentiment(tweet)
            tweet_data.append({
                'Tweet': tweet.text,
                'Sentiment': sentiment,
                'Date': tweet.created_at
            })

        # Convert to DataFrame for easy processing
        df = pd.DataFrame(tweet_data)

        # Generate summary report
        sentiment_summary = df['Sentiment'].value_counts().to_dict()

        return df, sentiment_summary

    def send_report_via_email(self, df, sentiment_summary):
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = outlook_email
        msg['To'] = recipient_email
        msg['Subject'] = f'Brand Sentiment Report: {self.brand_name} - {datetime.datetime.now().strftime("%Y-%m-%d")}'

        # Create email body with the sentiment analysis summary
        body = f"Brand: {self.brand_name}\n\n"
        body += "Sentiment Analysis Summary:\n"
        for sentiment, count in sentiment_summary.items():
            body += f"{sentiment}: {count} Tweets\n"

        body += "\nFull Tweet Details:\n"
        body += df.to_html(index=False)  # Convert DataFrame to HTML table

        msg.attach(MIMEText(body, 'html'))

        # Send email using Outlook's SMTP server
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(outlook_email, outlook_password)
            server.sendmail(outlook_email, recipient_email, msg.as_string())
            print("Email sent successfully!")


if __name__ == "__main__":
    # Initialize the BrandMonitoringAgent
    brand_agent = BrandMonitoringAgent('YourBrand')

    # Monitor and analyze the tweets
    tweet_data, sentiment_summary = brand_agent.monitor(100)

    # Send the sentiment analysis report via email
    brand_agent.send_report_via_email(tweet_data, sentiment_summary)
