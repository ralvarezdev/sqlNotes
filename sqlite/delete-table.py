import sqlite3

conn = sqlite3.connect('customer.db')

# Create a Cursor
c = conn.cursor()

# Delete from customers Table
c.execute("""
DELETE from customers WHERE username = 'ricardorosa'
""")

# Commit Command
conn.commit()

# Close Connection
conn.close()