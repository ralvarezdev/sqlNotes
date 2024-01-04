import sqlite3
from io import StringIO

conn = sqlite3.connect('customer.db')

# Create a Cursor
c = conn.cursor()

# Query the Database
# No Sorting
# c.execute("SELECT rowid, * FROM customers")

# Sort by Last Name in Ascending Order
# c.execute("SELECT rowid, * FROM customers ORDER BY last_name")

# ... and in Descending Order
c.execute("SELECT rowid, * FROM customers ORDER BY last_name DESC")

# Return First Item
# c.fetchone()

# Return N First Items
# c.fetchmany(2)

# Return All Items
items = c.fetchall()

msg = StringIO()
nChar = 15

# Print Header
msg.write("Row ID".ljust(nChar, ' ') + 
          "First Name".ljust(nChar, ' ') + 
          "Last Name".ljust(nChar, ' ') + 
          "Username".ljust(nChar, ' ') + 
          '\n')

# Add Separator
msg.write('-'*nChar*4)

# Loop Over Items
for item in items:
  msg.write('\n')

  # Append String to In-Memory Buffer with Left Alignment
  for value in item:
    try:
      msg.write(value.ljust(nChar, ' '))
    except:
      msg.write(str(value).ljust(nChar, ' '))

print(msg.getvalue())

# Query the Database Customer Row ID whose Username is ralvarez
c.execute("SELECT rowid FROM customers WHERE username = 'ralvarezdev'")

# First Match
ralvarezdev = c.fetchone()

# Print Row ID
print(f'\nRow ID of Customer whose Username is ralvarezdev: {ralvarezdev[0]}')

# Query the Database Customers whose First Name Starts with R or I
c.execute("SELECT first_name FROM customers WHERE first_name LIKE 'R%' OR first_name LIKE 'I%'")

# Query the Database Customers whose First Name Starts with R with a Limit of 2 Matches
# c.execute("SELECT first_name FROM customers WHERE first_name LIKE 'R%' LIMIT 2")

# Fetch All
like = c.fetchall()

# Print Customers First Name
print(f'\nCustomers whose First Name Starts with R or I: {like}')

# Commit Command
conn.commit()

# Close Connection
conn.close()