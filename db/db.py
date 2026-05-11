import sqlite3

# Connect to database
conn = sqlite3.connect("tickets.db")

# Create cursor
cursor = conn.cursor()

# Create tickets table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT,
    status TEXT
)
""")

print("Database and table created successfully!")

# Save changes
conn.commit()

# Close connection
conn.close()