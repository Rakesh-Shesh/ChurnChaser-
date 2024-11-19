# Import necessary libraries
import spacy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from sklearn.metrics.pairwise import cosine_similarity
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# Load spaCy model for advanced NLP
nlp = spacy.load("en_core_web_sm")

# Create a new instance of a ChatBot
bot = ChatBot('E-commerce ChatBot',
              logic_adapters=['chatterbot.logic.BestMatch'])

# Train the chatbot with a trainer
trainer = ChatterBotCorpusTrainer(bot)

# Train with English language corpus
trainer.train("chatterbot.corpus.english")

# Sample Product Data (Simulate E-Commerce Data)
product_catalog = {
    "Laptop": {
        "price": "$1000",
        "description": "A high-performance laptop for work and gaming."
    },
    "Smartphone": {
        "price": "$500",
        "description": "A sleek and powerful smartphone with an excellent camera."
    },
    "Headphones": {
        "price": "$100",
        "description": "Noise-cancelling headphones for an immersive listening experience."
    }
}

# Simulate E-commerce Order Data (For Order Tracking)
orders = {
    "12345": {"status": "Shipped", "tracking_number": "1Z23456789"},
    "67890": {"status": "Processing", "tracking_number": "1Z23456780"}
}


def send_email(subject, body, to_email="admin@example.com"):
    # Outlook Email Credentials
    from_email = "your_outlook_email@example.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


def get_product_recommendations(query):
    # Here, we use a simple keyword match to simulate recommendations
    query_nlp = nlp(query)
    recommendations = []

    for product, details in product_catalog.items():
        product_nlp = nlp(product)
        similarity = cosine_similarity([query_nlp.vector], [product_nlp.vector])
        if similarity > 0.5:  # Threshold for recommendation (can be adjusted)
            recommendations.append(f"{product}: {details['price']} - {details['description']}")

    return recommendations


def track_order(order_id):
    if order_id in orders:
        order = orders[order_id]
        return f"Order {order_id} is {order['status']}. Tracking Number: {order['tracking_number']}"
    else:
        return "Sorry, we couldn't find any order with that ID."


def ecommerce_chatbot():
    print("Hi, I'm your E-commerce Chatbot! How can I assist you today?")
    conversation_log = []

    while True:
        try:
            user_input = input()
            conversation_log.append(f"User: {user_input}")

            if user_input.lower() == 'quit':
                break

            if 'order' in user_input.lower() and 'status' in user_input.lower():
                order_id = user_input.split()[-1]
                response = track_order(order_id)
            elif 'recommend' in user_input.lower() or 'product' in user_input.lower():
                recommendations = get_product_recommendations(user_input)
                if recommendations:
                    response = "\n".join(recommendations)
                else:
                    response = "Sorry, I couldn't find any products that match your query."
            else:
                response = bot.get_response(user_input)

            conversation_log.append(f"Bot: {response}")
            print(response)

            # Periodically send email summary of the conversation
            if random.random() < 0.1:  # Send an email report 10% of the time
                subject = "Daily E-commerce Chatbot Interaction Summary"
                body = "\n".join(conversation_log)
                send_email(subject, body)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break


# Start the chatbot
if __name__ == "__main__":
    ecommerce_chatbot()
