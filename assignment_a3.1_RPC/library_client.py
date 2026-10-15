import rpyc

SERVER = "localhost"

PORT = 18861

   # ------------------- TESTS REMOVE BEFORE TURN IN --------------------------------
def show_response(label, response):
    print(f"\n--- {label} ---")
    print(response["message"])

    data = response["data"]
    if not response["success"] or data is None:
        return

    if isinstance(data, dict):
        print(data["book_id"],"|", data["title"], "| available:", data["available"])
    else:
        for book in data:
            print(book["book_id"],"|", book["title"], "| available:", book["available"])
# ---------------------------------------------------------------------------------

class Client:

    def run(self):

        
        connection = None
        
        try:

            connection = rpyc.connect(SERVER, PORT)

            print("Connected to the RPC server.")

            # response = connection.root.get_all_books()

            # if response["success"] and response["data"]:
              #  for book in response["data"]:
               #     print(book["book_id"], book["title"])
            
            # ------------------- TESTS REMOVE BEFORE TURN IN --------------------------------
            show_response("All books", connection.root.get_all_books())

            show_response("Search: gatsby", connection.root.search_book("gatsby"))
            show_response("Search: AUSTEN", connection.root.search_book("AUSTEN"))
            show_response("Search: zzz", connection.root.search_book("zzz"))
            show_response("Search: blank", connection.root.search_book("   "))

            show_response("Availability: book01", connection.root.check_availability("book01"))
            show_response("Availability: Book99", connection.root.check_availability("Book99"))
            show_response("Total books borrowed: ", connection.root.get_borrowed_books("S1001"))
            show_response("Total books borrowed: ", connection.root.get_borrowed_books("s1001"))
            show_response("Total books borrowed: ", connection.root.get_borrowed_books(" "))
            show_response("Total books borrowed: ", connection.root.get_borrowed_books("X101"))
            show_response("Total books borrowed: ", connection.root.get_borrowed_books("S12"))
            show_response("Check out a book: ", connection.root.borrow_book("S1001", "Book02"))
            show_response("Return a book: ", connection.root.return_book("S2002", "Book02"))
            show_response("Return a book: ", connection.root.return_book("S1001", "Book02"))
            show_response("Total books borrowed: ", connection.root.get_borrowed_books("S1001"))
            show_response("Return a book: ", connection.root.return_book("S1002", "Book02"))
            show_response("Return a book: ", connection.root.return_book("S1001", "Book99"))
            # ---------------------------------------------------------------------------------

        except ConnectionRefusedError:

            print("Connection failed. Start library_server.py first.")

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