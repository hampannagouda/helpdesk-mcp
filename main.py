from db.db import *

# Create table
create_table()

# Add tickets
create_ticket("Laptop not working", "High")
create_ticket("Email issue", "Medium")

# Show tickets
tickets = get_all_tickets()

print("\nAll Tickets:")
for ticket in tickets:
    print(ticket)

# Update status
update_ticket_status(1, "Resolved")

# Get single ticket
ticket = get_ticket_by_id(1)

print("\nSingle Ticket:")
print(ticket)

# Delete ticket
delete_ticket(2)