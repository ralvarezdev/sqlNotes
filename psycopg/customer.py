from psycopg import connect, sql
from io import StringIO

# Default Table Name
DEF_TABLENAME = "customers"

# Default ID Column Name
ROW_ID = "id"

# Default Database Class
class Database:
    # Protected Fields
    _host = None
    _dbname = None
    _user = None
    _password = None
    _port = None

    # Constructor
    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: int = 5432):         
        # Save Connection Data to Protected Fields
        self._host = host
        self._dbname = dbname
        self._user = user
        self._password = password
        self._port = port
        
        # Connect to Database
        self.conn = connect(
            host = host,
            dbname = dbname,
            user = user,
            password = password,
            port = port
        )
        self.c = self.getCursor()

    # Destructor
    def __del__(self):    
        # Commit Command
        self.conn.commit()

        # Close Connection
        if self.c is not None:
            self.c.close()
        if self.conn is not None:
            self.conn.close()

    # Get Cursor
    def getCursor(self):
        return self.conn.cursor()

# Customers Database Class
class Customers(Database):
    # Private Fields
    __mainTableName = None
    __items = None
    
    # Public Fields
    conn = None
    c = None
    
    # Get Main Table
    def getMainTable(self):
        return self.__mainTableName
    
    # Set Main Table
    def setMainTable(self, tableName: str):
        self.__mainTableName = tableName

    # Check Table Name
    def __checkTableName(self, tableName: str):
        # If the Table Name is None, returns the Main Table Name. Else, the Table Name
        if tableName is None:
            return self.__mainTableName
        return tableName

    # Method to Create Customers Table
    def createCustomersTable(self, tableName: str = DEF_TABLENAME):
        try:
            query = sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {tableName} (
                        {id} SERIAL PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        username TEXT)
                """).format(
                    tableName = sql.Identifier(tableName),
                    id = sql.Identifier(ROW_ID))

            # Execute Query
            self.c.execute(query)
            print(f"Table {tableName} Successfully Created\n")

            self.setMainTable(tableName)

        except Exception as err:
            print(err)

        # DATATYPES
        # - null
        # - integer
        # - real
        # - text
        # - blob (images, mp3 files)

    # Delete Customer from Table
    def deleteFromTable(self, field: str, value, tableName: str):
        query = sql.SQL(
                "DELETE FROM {tableName} WHERE {field} = (%s)"
            ).format(
                tableName = sql.Identifier(tableName), 
                field = sql.Identifier(field))
        
        try:
            self.c.execute(query, [value])
            print(f"Deleted Coincidences whose Field: '{field}' had {value} as Value\n")
        except Exception as err:
            print(err)

    # Drop Table
    def dropTable(self, tableName: str):
        query =  sql.SQL(
                "DROP TABLE IF EXISTS {tableName}"
            ).format(tableName = sql.Identifier(tableName))

        try:
            self.c.execute(query)
            print(f"Table {tableName} Successfully Dropped\n")
        except Exception as err:
            print(err)

    # Get Inset Customer to Table Query
    def __getInsertCustomerQuery(self, tableName: str):
        return sql.SQL(
                "INSERT INTO {tableName} (first_name, last_name, username) VALUES (%s, %s, %s)"
            ).format(tableName = sql.Identifier(tableName))

    # Insert Customer to Table
    def insertCustomer(self, customer: tuple, tableName: str = None):
        tableName = self.__checkTableName(tableName)
        
        query = self.__getInsertCustomerQuery()
        try:
            self.c.execute(query, customer)
            print(f"Customer Successfully Inserted to {tableName}\n")
        except Exception as err:
            print(err)
        
    # Insert Multiple Customers to Main Table
    def insertCustomers(self, customers: list, tableName: str = None):
        tableName = self.__checkTableName(tableName)

        query = self.__getInsertCustomerQuery(tableName)
        try:
            self.c.executemany(query, customers)
            print(f"Customers Successfully Inserted to {tableName}\n")
        except Exception as err:
            print(err)

    # Update Table with Row ID
    def updateCustomer(self, id: int, field: str, value, tableName: str = None):
        tableName = self.__checkTableName(tableName)

        # Cannot Modify ID Column Values
        if field == ROW_ID:
            print("Error: Cannot Modify {} Column Values\n".format(ROW_ID))
            return

        query = sql.SQL(
                "UPDATE {tableName} SET {field} = (%s) WHERE {rowid} = (%s)"
            ).format(
                rowid = sql.Identifier(ROW_ID),
                tableName = sql.Identifier(tableName),
                field = sql.Identifier(field))
        
        try:
            self.c.execute(query, [value, id])
            print(f"Customer {id} Successfully Updated to {tableName}\n")
        except Exception as err:
            print(err)

    # Order By Table
    def __orderBy(self, orderBy: str, desc: bool, tableName: str = None):
        tableName = self.__checkTableName(tableName)

        if desc:
            orderBy = orderBy.concat(' DESC')

        # Get Columns as a Representations of SQL Identifiers (Doesn't Work)
        """
        sqlCols = []
        for col in columns:
            sqlCols.append(sql.Identifier(col))
        """

        query = sql.SQL(
                    "SELECT * FROM {tableName} ORDER BY (%s)"
                ).format(
                    tableName = sql.Identifier(tableName))
        
        try:
            self.c.execute(query, [orderBy])
        except Exception as err:
            print(err)

        # Print Query
        # print(query.as_string(self.c))
        
    # Return All Items
    def __fetch(self, orderBy: str, desc: bool, tableName: str):
        try:
            self.__orderBy(orderBy, desc, tableName)
            self.__items = self.c.fetchall()
        except Exception as err:
            print(err)
            raise err

    # Print All Items from Main Table
    def printAll(self, orderBy: str = ROW_ID, desc: bool = False, nChar: int = 15, tableName: str = None):
        # Fetch Items
        try:
            self.__fetch(orderBy, desc, tableName)
        except Exception as err:
            raise err
            
        msg = StringIO()

        # Print Header
        msg.write("Row ID".ljust(nChar, ' ') + 
                "First Name".ljust(nChar, ' ') + 
                "Last Name".ljust(nChar, ' ') + 
                "Username".ljust(nChar, ' ') + 
                '\n')

        # Add Separator
        msg.write('-' * nChar * 4)

        # Check Items
        if self.__items is None:
            print("Error: No Items Fetched")
            return

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
