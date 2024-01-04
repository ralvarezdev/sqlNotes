import sqlite3

# Temp Database
# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('customer.db')

# Create a Cursor
c = conn.cursor()

# Create a Table
c.execute("""
CREATE TABLE customers (
    first_name text,
    last_name text,
    username text
)
""")

# DATATYPES
# - null
# - integer
# - real
# - text
# - blob (images, mp3 files)

# Commit Command
conn.commit()

# Close Connection
conn.close()