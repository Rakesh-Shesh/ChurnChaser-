import requests
from bs4 import BeautifulSoup
import csv
import logging
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pymysql
import json


class AutomatedWebScrapingAgent:
    def __init__(self, url, email_recipient=None):
        self.url = url
        self.email_recipient = email_recipient
        self.retry_count = 3
        self.retry_delay = 5  # seconds
        self.db_connection = self.connect_to_db()
        self.log_filename = 'scraper.log'
        logging.basicConfig(filename=self.log_filename, level=logging.INFO)

    def connect_to_db(self):
        # Connect to external database (e.g., MySQL or PostgreSQL)
        try:
            connection = pymysql.connect(
                host='localhost',
                user='user',
                password='password',
                database='scraped_data_db'
            )
            return connection
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def get_data(self):
        # Attempt to scrape the website with retry logic
        attempt = 0
        while attempt < self.retry_count:
            try:
                logging.info(f"Attempting to fetch data from {self.url}")
                response = requests.get(self.url)
                response.raise_for_status()  # Raise an exception for 4XX/5XX errors
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching data: {e}")
                attempt += 1
                time.sleep(self.retry_delay)
        raise Exception(f"Failed to fetch data from {self.url} after {self.retry_count} attempts.")

    def parse_data(self, soup):
        data = []
        # Assuming the data is in multiple tables with different structures
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                if cols:  # Ensure that we are not appending empty rows
                    data.append(cols)
        return data

    def write_to_csv(self, data, filename='output.csv'):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        logging.info(f"Data written to CSV file successfully: {filename}")
        return filename

    def save_to_db(self, data):
        # Save the data to a MySQL database
        try:
            cursor = self.db_connection.cursor()
            for row in data:
                # Assuming columns for 'id', 'name', 'price', 'category' (adjust based on your data)
                cursor.execute("INSERT INTO scraped_data (name, price, category) VALUES (%s, %s, %s)", row)
            self.db_connection.commit()
            logging.info("Data saved to database successfully.")
        except Exception as e:
            logging.error(f"Error saving data to database: {e}")

    def send_alert_email(self, subject, body):
        # Send an email alert to the user
        if self.email_recipient:
            try:
                msg = MIMEMultipart()
                msg['From'] = 'your_email@gmail.com'
                msg['To'] = self.email_recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('your_email@gmail.com', 'your_password')
                text = msg.as_string()
                server.sendmail('your_email@gmail.com', self.email_recipient, text)
                server.quit()
                logging.info("Alert email sent successfully.")
            except Exception as e:
                logging.error(f"Error sending email: {e}")

    def process_and_integrate_data(self, soup):
        data = self.parse_data(soup)

        # Optional: Perform data transformations (e.g., cleaning, price conversion)
        data = [row for row in data if row and len(row) >= 3]  # Filter out incomplete rows

        # Optionally save to DB
        self.save_to_db(data)

        # Optionally send an alert if new data meets business criteria
        self.send_alert_email("New Data Scraped", "New data has been scraped and processed successfully.")

        # Write to CSV
        csv_filename = self.write_to_csv(data)
        return csv_filename

    def run_scraping_process(self):
        try:
            soup = self.get_data()  # Fetch data from the URL
            csv_filename = self.process_and_integrate_data(soup)  # Process and save the data
            logging.info(f"Scraping and processing completed successfully. CSV file: {csv_filename}")
        except Exception as e:
            logging.error(f"Error during scraping process: {e}")


if __name__ == "__main__":
    url = 'http://www.example.com'  # replace with your target URL
    agent = AutomatedWebScrapingAgent(url, email_recipient="recipient@example.com")
    agent.run_scraping_process()
