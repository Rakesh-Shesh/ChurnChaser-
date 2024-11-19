import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import time


class ComplianceMonitoringAgent:
    def __init__(self, db_connection=None, email_config=None):
        self.compliance_rules = [
            self.rule_positive_numbers,
            self.rule_non_empty_strings,
            self.rule_valid_email_format,
            self.rule_data_within_range
        ]
        self.db_connection = db_connection
        self.email_config = email_config

    def rule_positive_numbers(self, data):
        """Rule: All numbers must be positive"""
        return all(number > 0 for number in data)

    def rule_non_empty_strings(self, data):
        """Rule: All strings must be non-empty"""
        return all(bool(item.strip()) for item in data if isinstance(item, str))

    def rule_valid_email_format(self, data):
        """Rule: Check if strings are valid email formats"""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return all(re.match(email_regex, item) for item in data if isinstance(item, str))

    def rule_data_within_range(self, data, min_value=1, max_value=100):
        """Rule: All numeric data must be within a specified range"""
        return all(min_value <= number <= max_value for number in data if isinstance(number, (int, float)))

    def check_compliance(self, data):
        """Check data for compliance with all rules"""
        return all(rule(data) for rule in self.compliance_rules)

    def fetch_data_from_db(self):
        """Fetch data from a database for compliance checking"""
        if not self.db_connection:
            return []

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM data_table")  # Example query, adjust as needed
        return cursor.fetchall()

    def send_compliance_alert(self, data):
        """Send an email alert if compliance is not met"""
        if not self.email_config:
            return

        from_email = self.email_config.get('from_email')
        to_email = self.email_config.get('to_email')
        password = self.email_config.get('password')

        subject = "Compliance Alert"
        body = f"The following data did not meet compliance rules: {data}"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            print(f"Alert sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def monitor_compliance_periodically(self, interval=60):
        """Monitor compliance at regular intervals"""
        while True:
            data = self.fetch_data_from_db()
            for entry in data:
                if not self.check_compliance(entry):
                    self.send_compliance_alert(entry)
            time.sleep(interval)


if __name__ == "__main__":
    # Email configuration for alerts
    email_config = {
        'from_email': 'youremail@gmail.com',
        'to_email': 'admin@example.com',
        'password': 'yourpassword'
    }

    # Example: Database connection setup
    db_connection = sqlite3.connect('example.db')

    # Create an instance of ComplianceMonitoringAgent
    agent = ComplianceMonitoringAgent(db_connection=db_connection, email_config=email_config)

    # Some test data
    test_data1 = [1, 2, 3]
    test_data2 = [-1, 'hello@example.com', '']
    test_data3 = [50, 150]

    # Check compliance of test data
    print(f"Compliance of test_data1: {agent.check_compliance(test_data1)}")
    print(f"Compliance of test_data2: {agent.check_compliance(test_data2)}")
    print(f"Compliance of test_data3: {agent.check_compliance(test_data3)}")

    # Start periodic compliance monitoring (every 60 seconds)
    agent.monitor_compliance_periodically()
