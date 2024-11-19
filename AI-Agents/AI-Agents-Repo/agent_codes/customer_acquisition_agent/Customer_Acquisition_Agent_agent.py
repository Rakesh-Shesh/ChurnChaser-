import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Customer Class
class Customer:
    def __init__(self, id, name, contact, address, email, signup_date=None):
        self.id = id
        self.name = name
        self.contact = contact
        self.address = address
        self.email = email
        self.signup_date = signup_date or datetime.datetime.now()


# Customer Acquisition Agent Class
class CustomerAcquisitionAgent:
    def __init__(self):
        self.customers = []
        self.email_server = "smtp.gmail.com"
        self.email_port = 587
        self.email_user = "your_email@gmail.com"
        self.email_password = "your_password"  # Use app-specific password if 2FA enabled

    def acquire_customer(self, id, name, contact, address, email):
        # Validate Email
        if not self.validate_email(email):
            print("Invalid email format!")
            return

        new_customer = Customer(id, name, contact, address, email)
        self.customers.append(new_customer)
        print(f"New customer {new_customer.name} has been acquired!")

        # Send a welcome email
        self.send_welcome_email(new_customer)

        # Automated Follow-Up
        self.schedule_follow_up(new_customer)

    def get_customer_details(self, id):
        for customer in self.customers:
            if customer.id == id:
                return vars(customer)
        return "Customer not found"

    def get_all_customers(self):
        return [vars(customer) for customer in self.customers]

    def validate_email(self, email):
        """Basic email validation"""
        return "@" in email and "." in email

    def send_welcome_email(self, customer):
        """Send a welcome email to the customer"""
        try:
            # Create the email content
            message = MIMEMultipart()
            message["From"] = self.email_user
            message["To"] = customer.email
            message["Subject"] = "Welcome to Our Service!"

            body = f"Dear {customer.name},\n\nThank you for signing up. We are thrilled to have you with us!\n\nBest regards,\nCustomer Support"
            message.attach(MIMEText(body, "plain"))

            # Send the email
            with smtplib.SMTP(self.email_server, self.email_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user, customer.email, message.as_string())

            print(f"Welcome email sent to {customer.email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def schedule_follow_up(self, customer):
        """Schedule a follow-up email reminder for the customer"""
        follow_up_time = customer.signup_date + datetime.timedelta(days=7)
        print(f"Follow-up scheduled for {customer.name} on {follow_up_time}")


# Example Usage
if __name__ == "__main__":
    agent = CustomerAcquisitionAgent()

    # Acquire new customers
    agent.acquire_customer(1, "John Doe", "1234567890", "123, Street, City", "john.doe@example.com")
    agent.acquire_customer(2, "Jane Doe", "0987654321", "456, Street, City", "jane.doe@example.com")

    # Fetch customer details
    print(agent.get_customer_details(1))
    print(agent.get_all_customers())
