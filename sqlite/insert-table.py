import sqlite3

conn = sqlite3.connect('customer.db')

# Create a Cursor
c = conn.cursor()

customers= [
    ('Ramon','Alvarez','ralvarezdev'),
    ('David', 'Ford', 'davidford'),
    ('Ivana', 'Honda', 'ivanahonda'),
    ('Roberto', 'Edison', 'robertoedison')
]

# Insert Single Customer
c.execute("""
INSERT INTO customers VALUES (
    'Ricardo', 'Rosa', 'ricardorosa'
)
""")

# Insert to Multiple Customers
c.executemany("INSERT INTO customers VALUES (?, ?, ?)", customers)

# Commit Command
conn.commit()

# Close Connection
conn.close()