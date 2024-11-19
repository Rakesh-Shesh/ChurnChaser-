# SurveyBot: A Survey Automation and Analytics Chatbot

SurveyBot is an intelligent survey automation chatbot that collects feedback from users, stores responses in a database, and sends the survey results via email to the admin. The bot uses natural language processing (NLP) to interact with users, validate their inputs, and provide valuable insights for business analytics.

## Features
- **Automated Survey Interaction**: The bot asks predefined survey questions and receives user responses.
- **Database Storage**: Survey responses are saved into an SQLite database for later analysis.
- **Email Notification**: After completing the survey, the results are emailed to the admin.
- **Input Validation**: Ensures that ratings are within a valid range (1-10).
- **Extensible**: Easily extendable for additional features, such as integrating with a CRM, analytics tools, or advanced sentiment analysis.

## Prerequisites
- Python 3.x
- Email account (Gmail recommended) for sending the survey results.
- SQLite (bundled with Python)

## Installation

### 1. Install Dependencies
Before running the project, you need to install the required libraries. You can install them via `pip`:

```bash
pip install chatterbot smtplib sqlite3
