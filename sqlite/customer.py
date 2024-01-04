import sqlite3
from io import StringIO

class CustomerDB:
    # Private Fields
    __defTableName = 'customers'
    __items = None

    # Constructor
    def __init__(self, databaseName, tableName = __defTableName):
        # Temp Database
        # conn = sqlite3.connect(':memory:')
    
        self.conn = sqlite3.connect(databaseName)
        self.mainTable = tableName
        self.c = self.getCursor()

    # Destructor
    def __del__(self):    
        # Commit Command
        self.conn.commit()

        # Close Connection
        self.conn.close()

    # Create a Cursor
    def getCursor(self):
        return self.conn.cursor()

    # Method to Create Customers Table
    def createCustomersTable(self, tableName = __defTableName):
        try:
            self.c.execute(f"""
                CREATE TABLE {tableName} (
                first_name text,
                last_name text,
                username text
                )
            """)
        except:
            print(f"Error: {tableName} Table Already Exists\n")

        # DATATYPES
        # - null
        # - integer
        # - real
        # - text
        # - blob (images, mp3 files)

    # Delete Customer from Table
    def deleteFromTable(self, field, value, tableName = __defTableName):
        self.c.execute(f"DELETE from {tableName} WHERE {field} = '{value}'")

    # Drop Table
    def dropTable(self, tableName = __defTableName):
        self.c.execute(f"DROP TABLE {tableName}")

    # Insert Multiple Customer to Table
    def insertCustomer(self, customer, tableName = __defTableName):
        self.c.execute(f"INSERT INTO {tableName} VALUES (?, ?, ?)", customer)
        
    # Insert Multiple Customers to Main Table
    def insertCustomers(self, customers, tableName = __defTableName):
        self.c.executemany(f"INSERT INTO {tableName} VALUES (?, ?, ?)", customers)

    # Update Table with Row ID
    def updateCustomer(self, rowid, field, value, tableName = __defTableName):
        self.c.execute(f"UPDATE {tableName} SET {field} = '{value}' WHERE rowid = {int(rowid)}")

    # Order By Table
    def __orderBy(self, field, desc, tableName):
       self.c.execute(f"SELECT rowid, * FROM {tableName} ORDER BY {field} {'DESC' if desc else ''}")

    # Return All Items
    def __fetch(self, field, desc, tableName):
        self.__orderBy(field, desc, tableName)
        self.__items = self.c.fetchall()

    # Print All Items from Main Table
    def printAll(self, field = 'rowid', desc = False, nChar = 15, tableName = __defTableName):
        # Fetch Items
        self.__fetch(field, desc, tableName)

        msg = StringIO()

        # Print Header
        msg.write("Row ID".ljust(nChar, ' ') + 
                "First Name".ljust(nChar, ' ') + 
                "Last Name".ljust(nChar, ' ') + 
                "Username".ljust(nChar, ' ') + 
                '\n')

        # Add Separator
        msg.write('-'*nChar*4)

        # Loop Over Items
        for item in self.__items:
            msg.write('\n')

            # Append String to In-Memory Buffer with Left Alignment
            for value in item:
                try:
                    msg.write(value.ljust(nChar, ' '))
                except:
                    msg.write(str(value).ljust(nChar, ' '))
        msg.write('\n')

        print(msg.getvalue())
