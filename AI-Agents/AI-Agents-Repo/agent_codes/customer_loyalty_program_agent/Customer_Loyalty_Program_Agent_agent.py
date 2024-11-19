
class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.points = 0

class CustomerLoyaltyProgramAgent:
    def __init__(self):
        self.customers = {}

    def add_customer(self, name, email):
        if email not in self.customers:
            self.customers[email] = Customer(name, email)
            print(f'Customer {name} added to the loyalty program.')
        else:
            print(f'Customer {name} is already in the loyalty program.')

    def add_points(self, email, points):
        if email in self.customers:
            self.customers[email].points += points
            print(f'{points} points added to customer {self.customers[email].name}.')
        else:
            print('Customer not found in the loyalty program.')

    def check_points(self, email):
        if email in self.customers:
            print(f'Customer {self.customers[email].name} has {self.customers[email].points} points.')
        else:
            print('Customer not found in the loyalty program.')

# Testing the AI agent
agent = CustomerLoyaltyProgramAgent()

# Adding some customers
agent.add_customer('John Doe', 'johndoe@example.com')
agent.add_customer('Jane Smith', 'janesmith@example.com')

# Adding points to the customers
agent.add_points('johndoe@example.com', 100)
agent.add_points('janesmith@example.com', 200)

# Checking the points of the customers
agent.check_points('johndoe@example.com')
agent.check_points('janesmith@example.com')
