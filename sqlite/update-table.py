import sqlite3

conn = sqlite3.connect('customer.db')

# Create a Cursor
c = conn.cursor()

# Update customers Table
c.execute("""
UPDATE customers SET first_name = 'Davis' WHERE rowid = 3
""")

# Commit Command
conn.commit()

# Close Connection
conn.close()