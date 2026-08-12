import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tickets.db")

# Ensure the containing folder exists before opening the database.
os.makedirs(BASE_DIR, exist_ok=True)

# -----------------------------
# Database Connection Function
# -----------------------------
def connect_db():
    return sqlite3.connect(DB_PATH)


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


# -----------------------------
# Create Ticket
# -----------------------------
def create_ticket(title, priority="Unassigned", status="Open"):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets (title, priority, status)
    VALUES (?, ?, ?)
    """, (title, priority, status))
    
    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return ticket_id


# -----------------------------
# Get All Tickets
# -----------------------------
def get_all_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, priority, status FROM tickets")

    tickets = [
        {"id": row[0], "title": row[1], "priority": row[2], "status": row[3]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return tickets


# -----------------------------
# Get Open Tickets
# -----------------------------
def get_open_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, priority, status FROM tickets WHERE status = 'Open'")

    # Map to dictionaries for better MCP tool output
    tickets = [
        {"ticket_id": row[0], "title": row[1], "priority": row[2], "status": row[3]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return tickets


# -----------------------------
# Get Ticket By ID
# -----------------------------
def get_ticket_by_id(ticket_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, priority, status FROM tickets WHERE id = ?
    """, (ticket_id,))

    row = cursor.fetchone()
    ticket = {"id": row[0], "title": row[1], "priority": row[2], "status": row[3]} if row else None

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


# -----------------------------
# Update Ticket Priority
# -----------------------------
def update_ticket_priority(ticket_id, new_priority):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tickets
    SET priority = ?
    WHERE id = ?
    """, (new_priority, ticket_id))

    conn.commit()
    conn.close()

# -----------------------------
# Generic Update Ticket
# -----------------------------
def update_ticket(ticket_id, updates):
    if not updates:
        return
    
    conn = connect_db()
    cursor = conn.cursor()

    fields = []
    values = []
    for key, value in updates.items():
        fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(ticket_id)
    
    query = f"UPDATE tickets SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(values))

    conn.commit()
    conn.close()


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


# -----------------------------
# Run Table Creation
# -----------------------------
if __name__ == "__main__":
    create_table()