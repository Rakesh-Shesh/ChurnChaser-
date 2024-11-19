
# Required Libraries
import datetime

class FinancialAnalystAgent:
    def __init__(self, name):
        self.name = name
        self.income = {}
        self.expenses = {}

    def add_income(self, source, amount):
        current_date = str(datetime.datetime.now().date())
        if current_date in self.income:
            self.income[current_date].append((source, amount))
        else:
            self.income[current_date] = [(source, amount)]

    def add_expense(self, item, amount):
        current_date = str(datetime.datetime.now().date())
        if current_date in self.expenses:
            self.expenses[current_date].append((item, amount))
        else:
            self.expenses[current_date] = [(item, amount)]
            
    def calculate_balance(self):
        total_income = sum(amount for date in self.income for source, amount in self.income[date])
        total_expenses = sum(amount for date in self.expenses for item, amount in self.expenses[date])
        return total_income - total_expenses

    def report(self):
        balance = self.calculate_balance()
        print(f"Hello! I am your Financial Analyst Agent, {self.name}.")
        print(f"Your current balance is: {balance}")
        print(f"Here is the detailed report of your income and expenses:")
        print(f"Income: {self.income}")
        print(f"Expenses: {self.expenses}")

# Test
if __name__ == '__main__':
    my_agent = FinancialAnalystAgent('John')
    my_agent.add_income('Salary', 5000)
    my_agent.add_expense('Rent', 1000)
    my_agent.add_expense('Groceries', 200)
    my_agent.report()
