import psycopg2
from simple_salesforce import Salesforce

class Product:
    def __init__(self, product_id, name, price, category=None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

    def update_price(self, new_price):
        self.price = new_price


class Catalog:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_product_from_db(self, product_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM products WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        if row:
            return Product(row[0], row[1], row[2], row[3])
        return None

    def add_product_to_db(self, product):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO products (product_id, name, price, category) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (product.product_id, product.name, product.price, product.category))
        self.db_connection.commit()

    def update_product_price_in_db(self, product):
        cursor = self.db_connection.cursor()
        query = "UPDATE products SET price = %s WHERE product_id = %s"
        cursor.execute(query, (product.price, product.product_id))
        self.db_connection.commit()


class Bill:
    def __init__(self):
        self.products = []
        self.tax_rate = 0.08  # Default 8% tax
        self.discount = 0.0  # No discount by default

    def add_product(self, product, quantity):
        self.products.append((product, quantity))

    def apply_discount(self, discount_percentage):
        self.discount = discount_percentage / 100.0

    def calculate_subtotal(self):
        subtotal = 0
        for product, quantity in self.products:
            subtotal += product.price * quantity
        return subtotal

    def calculate_total(self):
        subtotal = self.calculate_subtotal()
        tax = subtotal * self.tax_rate
        discount = subtotal * self.discount
        total = subtotal + tax - discount
        return total


class Customer:
    def __init__(self, customer_id, name, email=None):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.purchase_history = []

    def add_to_history(self, bill):
        self.purchase_history.append(bill)

    def get_purchase_history(self):
        return self.purchase_history


class AutomatedBillingAssistant:
    def __init__(self, catalog, db_connection, salesforce_instance):
        self.catalog = catalog
        self.db_connection = db_connection
        self.salesforce_instance = salesforce_instance
        self.bill = Bill()
        self.customer = None

    def set_customer(self, customer):
        self.customer = customer

    def add_product_to_bill(self, product_id, quantity):
        product = self.catalog.get_product_from_db(product_id)
        if product:
            self.bill.add_product(product, quantity)
        else:
            print(f"Product with ID {product_id} not found in catalog!")

    def apply_discount_to_bill(self, discount_percentage):
        self.bill.apply_discount(discount_percentage)

    def calculate_total_bill(self):
        return self.bill.calculate_total()

    def update_product_price(self, product_id, new_price):
        product = self.catalog.get_product_from_db(product_id)
        if product:
            product.update_price(new_price)
            self.catalog.update_product_price_in_db(product)

    def generate_receipt(self):
        if self.customer:
            self.customer.add_to_history(self.bill)
        total = self.calculate_total_bill()
        print(f"Receipt for {self.customer.name if self.customer else 'Guest'}")
        print(f"Subtotal: ${self.bill.calculate_subtotal():.2f}")
        print(f"Discount: ${self.bill.calculate_subtotal() * self.bill.discount:.2f}")
        print(f"Tax: ${self.bill.calculate_subtotal() * self.bill.tax_rate:.2f}")
        print(f"Total: ${total:.2f}")
        self.update_salesforce_order()

    def update_salesforce_order(self):
        # Updating Salesforce customer record and order information
        if self.customer:
            # Assuming you are creating a new order in Salesforce
            order_data = {
                'CustomerId': self.customer.customer_id,
                'TotalAmount': self.calculate_total_bill(),
                'Products': [(product.name, quantity) for product, quantity in self.bill.products]
            }
            self.create_salesforce_order(order_data)

    def create_salesforce_order(self, order_data):
        # Create a new order in Salesforce
        order = self.salesforce_instance.Order.create({
            'AccountId': order_data['CustomerId'],
            'TotalAmount': order_data['TotalAmount']
        })
        print(f"Created Salesforce order with ID: {order['id']}")
        for product_name, quantity in order_data['Products']:
            self.salesforce_instance.OrderItem.create({
                'OrderId': order['id'],
                'ProductName': product_name,
                'Quantity': quantity
            })
        print("Salesforce order and items created successfully")


# Usage:
# Set up the PostgreSQL connection
db_connection = psycopg2.connect(
    dbname="your_dbname",
    user="your_dbuser",
    password="your_dbpassword",
    host="localhost",
    port="5432"
)

# Set up Salesforce connection
sf = Salesforce(username='your_username', password='your_password', security_token='your_token')

# Create catalog and assistant
catalog = Catalog(db_connection)
assistant = AutomatedBillingAssistant(catalog, db_connection, sf)

# Set up customer
customer = Customer(customer_id='12345', name='John Doe', email='john.doe@example.com')
assistant.set_customer(customer)

# Example product and bill handling
assistant.add_product_to_bill('Apple', 10)
assistant.add_product_to_bill('Banana', 5)

# Apply discount and generate receipt
assistant.apply_discount_to_bill(10)
assistant.generate_receipt()
