# Brand Monitoring Agent with Sentiment Analysis and Email Reporting

## Overview
The **Brand Monitoring Agent** is a Python-based tool that monitors Twitter for mentions of a specified brand, performs sentiment analysis on the tweets, and sends a detailed report via Outlook email. The agent provides valuable insights by categorizing tweets as Positive, Neutral, or Negative, and summarizes the sentiment trends for the monitored brand.

## Features
- **Twitter Integration**: Fetches tweets related to a specified brand using the Twitter API.
- **Sentiment Analysis**: Uses **TextBlob** to analyze the sentiment of each tweet and categorize it as Positive, Neutral, or Negative.
- **Detailed Reporting**: Generates a comprehensive report with sentiment breakdown and full tweet details.
- **Email Notification**: Sends the report via **Outlook** email in HTML format for easy sharing and review.
- **Customizable**: Easily adjust the number of tweets to analyze, the brand name to monitor, and the recipient of the email report.

## Requirements
To run the project, you’ll need the following Python libraries:
- `tweepy` – For interacting with the Twitter API.
- `textblob` – For sentiment analysis.
- `pandas` – For managing tweet data and generating reports.
- `smtplib` – For sending email reports via Outlook.

You can install the required libraries using the following command:
```bash
pip install tweepy textblob pandas
