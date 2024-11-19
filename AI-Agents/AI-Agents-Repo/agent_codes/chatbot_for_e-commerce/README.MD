# E-commerce Chatbot with Advanced NLP and Order Tracking

## Overview
The **E-commerce Chatbot** is an AI-powered assistant designed to interact with users, provide product recommendations, track order statuses, and send email summaries of conversations to the admin. Built using **ChatterBot** for conversational AI and **spaCy** for advanced NLP tasks, the bot can also integrate with external systems, like an order management system, and periodically sends reports via email.

### Key Features:
- **Product Recommendation**: Uses NLP (spaCy) to suggest products based on user queries.
- **Order Tracking**: Allows users to track the status of their orders by providing an order ID.
- **E-commerce Insights**: Periodically sends email reports of user interactions to the admin.
- **Conversational AI**: Uses **ChatterBot** for handling general user queries and building conversations.

## Prerequisites

To run this chatbot, ensure you have the following:

- Python 3.x
- Internet connection for downloading necessary libraries and for email functionality.

### Required Libraries

- **ChatterBot**: For building the conversational AI engine.
- **spaCy**: For advanced NLP tasks and product recommendation based on query similarity.
- **sklearn**: For calculating cosine similarity between text.
- **smtplib**: For sending email reports.
- **textblob**: For sentiment analysis or further NLP enhancement (optional).

To install these libraries, use:

```bash
pip install chatterbot spacy sklearn smtplib
python -m spacy download en_core_web_sm
