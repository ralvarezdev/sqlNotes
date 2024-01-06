from customer import Customers

# First, I Created a Database Named as 'psycopg2-test' in pgAdmin4

host = "localhost"
dbname = "psycopg2-test" # Database Name
user = "postgres" # Default User
password = ""
port = 5432 # Default Port

# Initialize Class
db = Customers(dbname, user, password, host, port)

# Drop Table
db.dropTable('customers')

# Create Customers Table
db.createCustomersTable()

# Insert Customers to Table
customers = [
    ('Ramon','Alvarez','ralvarezdev'),
    ('David', 'Ford', 'davidford'),
    ('Ivana', 'Honda', 'ivanahonda'),
    ('Roberto', 'Edison', 'robertoedison')
]

db.insertCustomers(customers)

# Print Customers
db.printAll()

# Update Table
db.updateCustomer(3, 'username', 'pythonista')
db.printAll()

# Delete Customer from Table
db.deleteFromTable('username', 'ralvarezdev', 'customers')
db.printAll()

# Drop Table
db.dropTable('customers')