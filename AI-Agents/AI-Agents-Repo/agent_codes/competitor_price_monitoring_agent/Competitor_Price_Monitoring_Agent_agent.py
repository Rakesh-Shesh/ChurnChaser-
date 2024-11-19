import requests
from bs4 import BeautifulSoup
import time
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class CompetitorPriceMonitor:
    def __init__(self, urls, output_file, email_config, alert_threshold=10):
        self.urls = urls
        self.output_file = output_file
        self.email_config = email_config
        self.alert_threshold = alert_threshold  # percentage drop for alerts
        self.previous_prices = {}

    def get_product_details(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            product_name = soup.find('h1', {'class': 'product-title'}).text.strip()
            product_price = float(soup.find('span', {'class': 'product-price'}).text.strip().replace('$', '').replace(',', ''))

            return {
                'product_name': product_name,
                'product_price': product_price,
                'url': url
            }
        except Exception as e:
            print(f"Failed to get details for {url}, error: {e}")
            return None

    def monitor_prices(self):
        while True:
            with open(self.output_file, 'a') as f:
                writer = csv.DictWriter(f, fieldnames=['product_name', 'product_price', 'url', 'timestamp'])
                writer.writeheader()

                for url in self.urls:
                    product_details = self.get_product_details(url)
                    if product_details:
                        # Check if price has dropped significantly
                        self.check_price_drop(product_details)

                        # Write details to the CSV file
                        product_details['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow(product_details)

            # Send daily report email
            self.send_daily_report()

            # Sleep for a day
            time.sleep(24 * 60 * 60)

    def check_price_drop(self, product_details):
        product_name = product_details['product_name']
        current_price = product_details['product_price']

        if product_name in self.previous_prices:
            previous_price = self.previous_prices[product_name]
            price_diff = previous_price - current_price
            price_drop_percentage = (price_diff / previous_price) * 100

            if price_drop_percentage >= self.alert_threshold:
                # Send an alert email about the price drop
                self.send_price_drop_alert(product_name, previous_price, current_price)

        # Update the previous price
        self.previous_prices[product_name] = current_price

    def send_price_drop_alert(self, product_name, previous_price, current_price):
        subject = f"Price Drop Alert: {product_name}"
        body = f"The price for '{product_name}' has dropped from ${previous_price} to ${current_price}."

        self.send_email(subject, body)

    def send_daily_report(self):
        subject = "Competitor Price Monitoring Daily Report"
        body = "Here is the daily report on competitor prices.\n\n"
        body += self.get_daily_report()

        self.send_email(subject, body)

    def get_daily_report(self):
        report = ""
        for product_name, previous_price in self.previous_prices.items():
            report += f"Product: {product_name} - Last Price: ${previous_price}\n"

        return report

    def send_email(self, subject, body):
        from_email = self.email_config['from_email']
        to_email = self.email_config['to_email']
        password = self.email_config['password']

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email via Gmail SMTP server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"Failed to send email, error: {e}")

if __name__ == "__main__":
    urls = [
        'https://www.example.com/product1',
        'https://www.example.com/product2',
        # Add more URLs as needed
    ]
    email_config = {
        'from_email': 'youremail@gmail.com',
        'to_email': 'admin@example.com',
        'password': 'yourpassword'
    }
    monitor = CompetitorPriceMonitor(urls, 'prices.csv', email_config)
    monitor.monitor_prices()
