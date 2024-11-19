import smtplib
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

# Create a new instance of a ChatBot
bot = ChatBot('SurveyBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(bot)

# Train the chatbot based on the English corpus
trainer.train("chatterbot.corpus.english")

# Define survey questions
survey_questions = [
    "What is your name?",
    "How old are you?",
    "Where are you from?",
    "What is your profession?",
    "How do you rate our service from 1-10?"
]


# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('survey_responses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS responses
                      (name TEXT, age INTEGER, location TEXT, profession TEXT, rating INTEGER)''')
    conn.commit()
    conn.close()


def save_to_db(response_data):
    conn = sqlite3.connect('survey_responses.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO responses (name, age, location, profession, rating) VALUES (?, ?, ?, ?, ?)',
                   response_data)
    conn.commit()
    conn.close()


# Validate user input for rating
def validate_rating(rating):
    try:
        rating = int(rating)
        if 1 <= rating <= 10:
            return True
        else:
            return False
    except ValueError:
        return False


# Function to send the survey result via email
def send_email(response_data):
    from_email = "your_email@example.com"
    to_email = "admin@example.com"
    password = "your_email_password"

    # Create email content
    subject = "Survey Results"
    body = f"Survey completed:\n\nName: {response_data[0]}\nAge: {response_data[1]}\nLocation: {response_data[2]}\nProfession: {response_data[3]}\nRating: {response_data[4]}"

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Survey results sent to admin via email.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


# Conduct survey by asking questions and getting responses
def conduct_survey():
    print("Welcome to our survey. Your responses are invaluable to us.")
    responses = []

    for question in survey_questions:
        print(question)
        response = input()

        # If the question asks for rating, validate the response
        if question == survey_questions[-1]:  # Last question is rating
            while not validate_rating(response):
                print("Please provide a valid rating between 1 and 10.")
                response = input()

        responses.append(response)
        print("Chatbot: Thank you for your response.")

    save_to_db(responses)  # Save to the database
    send_email(responses)  # Send results to the admin via email
    print("Survey completed. Thank you for your time!")


if __name__ == "__main__":
    init_db()  # Initialize the database
    conduct_survey()  # Start the survey process
