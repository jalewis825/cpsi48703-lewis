import rpyc

SERVER = "localhost"

PORT = 18861

def display_response(response):
    print(response["message"])

    data = response["data"]
    if not response["success"] or data is None:
        return

    if isinstance(data, dict):
        data = [data]

    for book in data:
        status = "Available" if book["available"] else "Checked Out"
        print(f" {book['book_id']} | {book['title']} | {book['author']}| {status}" )

class Client:

    def run(self):

        connection = None
        
        try:
            connection = rpyc.connect(SERVER, PORT)
            print("Connected to the RPC server.")

            while True:
                print("\n------Library Menu------")
                print("1. Display all books")
                print("2. Search for a book by keyword")
                print("3. Check availability")
                print("4. Borrow a book")
                print("5. Return a book")
                print("6. View my borrowed books")
                print("7. Exit")

                choice = input("Enter your choice (1-7): ").strip()

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

        except ConnectionRefusedError:
            print("Connection failed. Start library_server.py first.")

        except EOFError:
            print("Lost connection to the server. Please restart the server and try again.")
            
        except Exception as error:
            print(f"An error occurred: {error}")

        finally:
            if connection is not None:
                connection.close()
                print("Connection closed.")

def main():

    client = Client()

    client.run()

if __name__ == "__main__":


    main()