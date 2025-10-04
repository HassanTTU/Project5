import sqlite3

# Notes 10/4/2025

# This connects to the database, (we will create since we don't have)
connection = sqlite3.connect('customers.db')
cursor = connection.cursor()

# Create the table, TEXT, UNIQUE, etc these are RULES
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        birthday TEXT,
        email TEXT UNIQUE,
        phone TEXT UNIQUE,
        address TEXT,
        preferred_contact TEXT
    )
''')

print("\nTable initialized successfully!\n")

# List of my customers to add
customers = [
    ("John Isaac", "Sep 4 2005", "jisaac98@outmail.com", "555-801-9877", "185 Main St", "Email"),
    ("Leanne Smith", "Dec 8 1989", "leannesmth42@dmail.com", "555-143-8051", "381 Oak Ave", "Phone"),
    ("Ryan Holsberg", "Jan 18 1975", "bigman45@email.com", "555-501-1097", "213 Pine Rd", "Phone"),
    ("Elizabeth Chris", "July 23 2002", "lizchris004@dmail.com", "555-700-1284", "44 Birch Blvd", "Email"),
    ("Idris Haydar", "Oct 11 1999", "aihaydar@email.com", "555-945-7301", "855 Cedar St", "Email")
]

# Insert customers from list, without duplicating each run *IMPORTANT
for customer in customers:
    try:
        cursor.execute('''
            INSERT INTO customers (name, birthday, email, phone, address, preferred_contact)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', customer)
        print(f"Added: {customer[0]}")
    except sqlite3.IntegrityError:
        print(f"Skipped duplicate: {customer[0]} ({customer[2]}, {customer[3]})")

# Save 
connection.commit()

# Show list
print("\nFinal list of customers in database:\n")
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

for row in rows:
    print(row)

print()
connection.close()
