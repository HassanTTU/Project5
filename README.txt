
#delete data

import sqlite3

conn = sqlite3.connect('customers.db')
cur = conn.cursor()

# Delete all rows from the table
cur.execute("DELETE FROM customers")

# Reset the AUTOINCREMENT counter
cur.execute("DELETE FROM sqlite_sequence WHERE name='customers'")

conn.commit()
conn.close()

print("✅ All customer data deleted and ID counter reset.")






#This is my first attempt with notes, 
#what I did wrong was already enter the sample data 


import sqlite3
import tkinter

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





###########################################Second try


import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to the database
conn = sqlite3.connect('customers.db')
cur = conn.cursor()

# Create the table
cur.execute('''
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
conn.commit()

# Delete duplicates (keep first entry only)
cur.execute('''
    DELETE FROM customers
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM customers
        GROUP BY email
    )
''')
cur.execute('''
    DELETE FROM customers
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM customers
        GROUP BY phone
    )
''')
conn.commit()

# GUI setup
win = tk.Tk()
win.title("Customer Info Form")
win.geometry("500x600")  # 👈 Makes the window bigger

# Input fields
labels = ["Name", "Birthday", "Email", "Phone", "Address"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(win, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=8, sticky="e")
    entry = tk.Entry(win, width=35, font=("Arial", 12))
    entry.grid(row=i, column=1, padx=10, pady=8)
    entries[label] = entry

# Dropdown for preferred contact
tk.Label(win, text="Preferred Contact", font=("Arial", 12)).grid(row=len(labels), column=0, padx=10, pady=8, sticky="e")
contact = tk.StringVar()
contact.set("Email")
tk.OptionMenu(win, contact, "Email", "Phone", "Mail").grid(row=len(labels), column=1, padx=10, pady=8)

# Input for ID to delete
tk.Label(win, text="Delete by ID", font=("Arial", 12)).grid(row=len(labels)+1, column=0, padx=10, pady=8, sticky="e")
delete_id_entry = tk.Entry(win, width=35, font=("Arial", 12))
delete_id_entry.grid(row=len(labels)+1, column=1, padx=10, pady=8)

# Submit function
def submit():
    data = tuple(entries[label].get() for label in labels) + (contact.get(),)
    if not all(data):
        messagebox.showwarning("Missing Info", "Please fill out all fields.")
        return
    try:
        cur.execute('''
            INSERT INTO customers (name, birthday, email, phone, address, preferred_contact)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        messagebox.showinfo("Success", "Customer added!")
        for entry in entries.values():
            entry.delete(0, tk.END)
        contact.set("Email")
    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate", "Email or phone already exists.")

# View all customers
def view_customers():
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    print("\n📋 All Customers:\n")
    for row in rows:
        print(row)

# Delete by ID
def delete_by_id():
    id_value = delete_id_entry.get()
    if not id_value.isdigit():
        messagebox.showwarning("Invalid ID", "Please enter a valid numeric ID.")
        return
    cur.execute("DELETE FROM customers WHERE id = ?", (id_value,))
    conn.commit()
    messagebox.showinfo("Deleted", f"Customer with ID {id_value} deleted.")
    delete_id_entry.delete(0, tk.END)

# Buttons
tk.Button(win, text="Submit", command=submit, font=("Arial", 12)).grid(row=len(labels)+2, column=0, columnspan=2, pady=12)
tk.Button(win, text="View All (prints to console)", command=view_customers, font=("Arial", 12)).grid(row=len(labels)+3, column=0, columnspan=2, pady=8)
tk.Button(win, text="Delete by ID", command=delete_by_id, font=("Arial", 12)).grid(row=len(labels)+4, column=0, columnspan=2, pady=8)

# Run the GUI
win.mainloop()
conn.close()