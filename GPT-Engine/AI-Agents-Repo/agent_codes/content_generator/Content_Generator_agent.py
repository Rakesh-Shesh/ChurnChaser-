import markovify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import logging
import time

# Setup logging for content generation
logging.basicConfig(filename='content_generator.log', level=logging.INFO)

class ContentGenerator:
    def __init__(self, text, email_config=None):
        self.text = text
        self.model = self.build_model()
        self.email_config = email_config

    def build_model(self):
        """Build a Markov Chain model based on the provided text."""
        return markovify.Text(self.text)

    def generate_sentence(self):
        """Generate a sentence using the Markov model."""
        sentence = self.model.make_sentence()
        logging.info(f"Generated sentence: {sentence}")
        return sentence

    def generate_paragraph(self, num_sentences=5):
        """Generate a paragraph with multiple sentences."""
        paragraph = ' '.join(self.generate_sentence() for _ in range(num_sentences))
        logging.info(f"Generated paragraph: {paragraph}")
        return paragraph

    def send_email(self, subject, body):
        """Send an email with the generated content."""
        if self.email_config is None:
            print("Email configuration is not set. Skipping email sending.")
            return

        # Email setup
        from_email = self.email_config['from_email']
        to_email = self.email_config['to_email']
        password = self.email_config['password']
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            # Set up the server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Start TLS encryption
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            logging.info(f"Email sent successfully to {to_email}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            print(f"Failed to send email: {e}")

    def fetch_external_content(self, url):
        """Fetch content from a URL and add it to the model."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                external_text = response.text
                self.text += external_text  # Append external content to internal text
                self.model = self.build_model()  # Rebuild model with new content
                logging.info(f"Successfully fetched content from {url}")
            else:
                logging.error(f"Failed to fetch content from {url}, Status Code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error fetching content from {url}: {e}")

    def run_periodic_content_generation(self, interval_minutes=60):
        """Generate content periodically and send it via email."""
        while True:
            content = self.generate_paragraph()
            self.send_email("New Content Generated", content)
            logging.info("Sent new generated content via email.")
            time.sleep(interval_minutes * 60)  # Wait for the specified interval before generating again

if __name__ == "__main__":
    email_config = {
        'from_email': 'youremail@gmail.com',
        'to_email': 'recipient@example.com',
        'password': 'yourpassword'
    }

    # Initialize the content generator
    text = """
    Artificial Intelligence is transforming industries, and content generation is one of the most exciting applications. 
    AI-generated content is revolutionizing marketing, journalism, and creative writing.
    """
    generator = ContentGenerator(text, email_config=email_config)

    # Optionally, fetch external content to improve the model (e.g., from a blog or website)
    generator.fetch_external_content("https://example.com/some-content")

    # Generate content and send it via email
    generator.run_periodic_content_generation(interval_minutes=5)  # Generate content every 5 minutes
