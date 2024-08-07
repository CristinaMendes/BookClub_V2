import mysql.connector
from mysql.connector import Error

class DatabaseHandler:
    def __init__(self, host='localhost', database='bookclub', user='root', port = 3307):
        # Attempt to establish a connection to the MySQL database
        try:
            self.conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                port=port
            )
            self.cursor = self.conn.cursor() # Create a cursor object for executing SQL commands
        except Error as e:
            # If an error occurs, print the error message and set conn and cursor to None
            print(f"Error: {e}")
            self.conn = None
            self.cursor = None
    
    def insert_book(self, book):
        # Check if the connection to the database is available
        if self.conn is None:
            print("No connection available.")
            return
        try:
            # Prepare and execute the SQL INSERT statement to add a new book record
            self.cursor.execute('''
                INSERT INTO book (title, category, rating, price, stock)
                VALUES (%s, %s, %s, %s, %s)
            ''', (book.title, book.category, book.rating, book.price, book.stock))
            self.conn.commit() # Commit the transaction to make changes persistent
        except Error as e:
            # If an error occurs during the insertion, print the error message
            print(f"Error: {e}")

    def close(self):
        # Close the cursor if it is not None
        if self.cursor is not None:
            self.cursor.close()
        # Close the connection to the database if it is not None and still connected
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            print("MySQL connection is closed")