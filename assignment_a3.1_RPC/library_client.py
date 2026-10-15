"""
library_client.py

Menu-driven RPC client for the Distributed Library Management System
(Assignment 3.1). Connects to the library server using the RPyC library
and calls its remote procedures based on user input. The client never
accesses the inventory directly; every operation goes through the server.

Based on the course example "Python 3.1.4 - RPC-based Client and Server
using RPyC Library." The example's connection setup and try/except/finally
error handling were kept. Its hard-coded append calls used for testing 
were replaced with a menu loop that collects user input and calls the six
library procedures, a shared function for displaying server responses was
added, and handling for a lost server connection mid-session was added.

Run with: python library_client.py (start library_server.py first)
"""

import rpyc

SERVER = "localhost"

PORT = 18861

# Prints the server's message, then any book records it returned.
def display_response(response):
    print(response["message"])

    data = response["data"]
    if not response["success"] or data is None:
        return

    if isinstance(data, dict):
        data = [data]

    for book in data:
        status = "Available" if book["available"] else "Checked Out"
        print(f" {book['book_id']} | {book['title']} | {book['author']} | {status}" )

# Handles the server connection and the library menu.
class Client:

    # Connects to the server, runs the menu until the user exits, then closes the connection.
    def run(self):

        connection = None
        
        try:
            connection = rpyc.connect(SERVER, PORT)
            print("Connected to the RPC server.")

            # Reapeat the meanu until the user chooses to exit
            while True:
                print("\n------Library Menu------")
                print("1. Display all books")
                print("2. Search for a book by keyword")
                print("3. Check availability")
                print("4. Borrow a book")
                print("5. Return a book")
                print("6. View my borrowed books")
                print("7. Exit")

                # Read the menu choice as text: invalid input is handled by the final else.
                choice = input("Enter your choice (1-7): ").strip()

                # Input is passed to the server as typed; the server cleans and validates it.

                if choice == "1":
                    display_response(connection.root.get_all_books())

                elif choice == "2":
                    keyword = input("Enter keyword: ")
                    display_response(connection.root.search_book(keyword))

                elif choice == "3":
                    book_id = input("Enter book ID: ")
                    display_response(connection.root.check_availability(book_id))

                elif choice == "4":
                    student_id = input("Enter student ID: ") 
                    book_id = input("Enter book ID: ")
                    display_response(connection.root.borrow_book(student_id, book_id))

                elif choice == "5":
                    student_id = input("Enter student ID: ") 
                    book_id = input("Enter book ID: ")
                    display_response(connection.root.return_book(student_id, book_id))

                elif choice == "6":
                    student_id = input("Enter student ID: ")
                    display_response(connection.root.get_borrowed_books(student_id))

                elif choice == "7":
                    print("Goodbye.")
                    break

                else:
                    print("Invalid choice. Please enter a number 1 to 7.")

        # Server was not running when the client started.
        except ConnectionRefusedError:
            print("Connection failed. Start library_server.py first.")

        # Server stopped while the client was running.
        except EOFError:
            print("Lost connection to the server. Please restart the server and try again.")

        # Any other unexpected error, so the client never crashes.
        except Exception as error:
            print(f"An error occurred: {error}")

        # Always close the connection, whether the client exited normally or after an error.
        finally:
            if connection is not None:
                connection.close()
                print("Connection closed.")

# Creates the client and starts it.
def main():

    client = Client()

    client.run()

if __name__ == "__main__":


    main()