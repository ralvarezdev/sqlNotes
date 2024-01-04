import sqlite3

conn = sqlite3.connect('customer.db')

# Create a Cursor
c = conn.cursor()

# Drop customers Table
c.execute("""
DROP TABLE customers
""")

# Commit Command
conn.commit()

# Close Connection
conn.close()