from customer import CustomerDB

customers = [
    ('Ramon','Alvarez','ralvarezdev'),
    ('David', 'Ford', 'davidford'),
    ('Ivana', 'Honda', 'ivanahonda'),
    ('Roberto', 'Edison', 'robertoedison')
]
"""
"""

# Initialize Class
db = CustomerDB('customerClass')

# Create Customers Table
db.createCustomersTable()

# Insert Customers to Table
db.insertCustomers(customers)

# Print Customers
db.printAll()

# Update Table
db.updateCustomer(3, 'username', 'pythonista')
db.printAll()

# Delete Customer from Table
db.deleteFromTable('username', 'ralvarezdev')
db.printAll()

# Drop Table
db.dropTable()
    
try:
    # Will Fail
    db.printAll()
except:
    print("Table Successfully Deleted")