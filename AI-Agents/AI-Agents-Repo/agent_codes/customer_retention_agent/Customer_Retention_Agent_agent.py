
# Importing required libraries
import random

class CustomerRetentionAgent:
    def __init__(self, name):
        self.name = name

    def respond(self, customer):
        """Generate a response to the customer based on their feedback."""
        if customer.satisfaction < 3:
            return self.apologize(customer)
        elif customer.satisfaction < 5:
            return self.offer_discount(customer)
        else:
            return self.thank(customer)

    def apologize(self, customer):
        """Apologize to the customer."""
        return f"We're sorry to hear that you're not satisfied with our service, {customer.name}. We'll do our best to improve."

    def offer_discount(self, customer):
        """Offer the customer a discount."""
        discount = random.choice([10, 20, 30])
        return f"As a token of our appreciation for your feedback, we'd like to offer you a {discount}% discount on your next purchase, {customer.name}."

    def thank(self, customer):
        """Thank the customer for their positive feedback."""
        return f"Thank you for your positive feedback, {customer.name}! We're glad to hear that you're satisfied with our service."


# Example usage:
class Customer:
    def __init__(self, name, satisfaction):
        self.name = name
        self.satisfaction = satisfaction  # On a scale from 1 to 5

agent = CustomerRetentionAgent('Customer Retention Agent')
customer1 = Customer('John Doe', 2)
customer2 = Customer('Jane Doe', 4)
customer3 = Customer('Bob Smith', 5)

print(agent.respond(customer1))
print(agent.respond(customer2))
print(agent.respond(customer3))
