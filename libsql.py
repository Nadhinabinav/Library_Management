import sqlite3

# Class to handle the Library operations
class Library:
    def __init__(self, list_of_books):
        self.books = list_of_books
        self.create_database()

    def create_database(self):
        # Connect to SQLite database (or create it)
        self.conn = sqlite3.connect('library_management.db')
        self.cursor = self.conn.cursor()
        
        # Create a table for storing operations (if not exists)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS operations (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               book_name TEXT NOT NULL,
                               operation TEXT NOT NULL,
                               user TEXT NOT NULL,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def display_books(self):
        print("\nBooks available in the library:")
        for book in self.books:
            print(f"- {book}")
    
    def borrow_book(self, book_name, user):
        if book_name in self.books:
            print(f"\nYou have borrowed '{book_name}'. Please return it on time.")
            self.books.remove(book_name)
            # Log the borrow operation in the database
            self.cursor.execute("INSERT INTO operations (book_name, operation, user) VALUES (?, ?, ?)", 
                                (book_name, 'borrowed', user))
            self.conn.commit()
        else:
            print(f"\nSorry, '{book_name}' is not available in the library.")
    
    def return_book(self, book_name, user):
        print(f"\nThank you for returning '{book_name}'.")
        self.books.append(book_name)
        # Log the return operation in the database
        self.cursor.execute("INSERT INTO operations (book_name, operation, user) VALUES (?, ?, ?)", 
                            (book_name, 'returned', user))
        self.conn.commit()

    def display_operations(self):
        print("\nLibrary Operations Log:")
        self.cursor.execute("SELECT * FROM operations")
        operations = self.cursor.fetchall()
        for op in operations:
            print(f"ID: {op[0]}, Book: {op[1]}, Operation: {op[2]}, User: {op[3]}, Time: {op[4]}")

class Student:
    def request_book(self):
        self.book = input("\nEnter the name of the book you want to borrow: ")
        return self.book
    
    def return_book(self):
        self.book = input("\nEnter the name of the book you want to return: ")
        return self.book

def main():
    library = Library(["Python Programming", "Data Structures", "Algorithms", "AI and ML"])
    student = Student()

    while True:
        print("\n===== Library Menu =====")
        print("1. Display all available books")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. View operations log")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            library.display_books()

        elif choice == 2:
            user = input("Enter your name: ")
            requested_book = student.request_book()
            library.borrow_book(requested_book, user)

        elif choice == 3:
            user = input("Enter your name: ")
            returned_book = student.return_book()
            library.return_book(returned_book, user)

        elif choice == 4:
            library.display_operations()

        elif choice == 5:
            print("\nThank you for using the library management system!")
            break
        
        else:
            print("\nInvalid choice! Please choose a valid option.")

if __name__ == "__main__":
    main()
