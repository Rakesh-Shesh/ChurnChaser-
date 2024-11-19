
class Ticket:
    def __init__(self, id, subject, description):
        self.id = id
        self.subject = subject
        self.description = description

class CustomerSupportTicketRoutingAgent:
    def __init__(self):
        self.departments = ["Sales", "Technical", "Billing"]

    def route_ticket(self, ticket):
        if "payment" in ticket.subject.lower() or "bill" in ticket.subject.lower():
            return self.departments[2]
        elif "broken" in ticket.subject.lower() or "error" in ticket.subject.lower():
            return self.departments[1]
        elif "purchase" in ticket.subject.lower() or "product" in ticket.subject.lower():
            return self.departments[0]
        else:
            return "General"

if __name__ == "__main__":
    agent = CustomerSupportTicketRoutingAgent()

    tickets = [Ticket(1, "Payment issue", "I have a problem with my last payment"),
               Ticket(2, "Product inquiry", "I want to know more about the product"),
               Ticket(3, "Broken feature", "One feature in your app is not working")]

    for ticket in tickets:
        print(f"Ticket {ticket.id} is routed to {agent.route_ticket(ticket)} department.")
