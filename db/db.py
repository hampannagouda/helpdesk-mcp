import sqlite3


# -----------------------------
# Database Connection Function
# -----------------------------
def connect_db():
    return sqlite3.connect("tickets.db")


# -----------------------------
# Create Table
# -----------------------------
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Tickets table ready!")


# -----------------------------
# Create Ticket
# -----------------------------
def create_ticket(title, priority, status="Open"):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets (title, priority, status)
    VALUES (?, ?, ?)
    """, (title, priority, status))

    conn.commit()
    conn.close()

    print("Ticket created successfully!")


# -----------------------------
# Get All Tickets
# -----------------------------
def get_all_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")

    tickets = cursor.fetchall()

    conn.close()

    return tickets


# -----------------------------
# Get Ticket By ID
# -----------------------------
def get_ticket_by_id(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tickets WHERE id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()

    conn.close()

    return ticket


# -----------------------------
# Update Ticket Status
# -----------------------------
def update_ticket_status(ticket_id, new_status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tickets
    SET status = ?
    WHERE id = ?
    """, (new_status, ticket_id))

    conn.commit()
    conn.close()

    print("Ticket status updated!")


# -----------------------------
# Delete Ticket
# -----------------------------
def delete_ticket(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM tickets
    WHERE id = ?
    """, (ticket_id,))

    conn.commit()
    conn.close()

    print("Ticket deleted successfully!")


# -----------------------------
# Run Table Creation
# -----------------------------
if __name__ == "__main__":
    create_table()