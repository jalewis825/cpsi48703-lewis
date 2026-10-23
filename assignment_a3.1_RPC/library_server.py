"""
library_server.py

Assignment 3.1: Distributed Library Management System - RPC

Author: Jessi Lewis
Course: CPSI 48703-9S1 - Distributed Computing
Date: 14-OCT-2026

RPC server for the Distributed Library Management System (Assignment 3.1).
Maintains the shared book inventory and exposes six remote procedures
(display, search, check availability, borrow, return, view borrowed books)
using the RPyC library. A threading lock keeps the inventory consistent
when multiple clients borrow or return books at the same time.

Based on the course example "Python 3.1.4 - RPC-based Client and Server
using RpyC Library." The example's service structure, ThreadedServer setup,
and connection handlers were kept. The per-client list was replaced with a
shared library inventory, the example's append and get_value procedures 
were replaced with the six library procedures, and input validation, a
consisten response format, and locking for borrow and return were added. 

Run with: python library_server.py
"""
import threading

import rpyc

from rpyc.utils.server import ThreadedServer

SERVER = "localhost"

PORT = 18861

# Shared inventory: built once at startup so every client see the same books.
library = {
    "Book01":{
        "book_id": "Book01",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "available" : True,
        "borrower_id": None, 
    },

    "Book02":{
        "book_id": "Book02",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book03":{
        "book_id": "Book03",
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "available": True,
        "borrower_id": None, 
    },    
    
    "Book04":{
        "book_id": "Book04",
        "title": "The Road",
        "author": "Cormac McCarthy",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book05":{
        "book_id": "Book05",
        "title": "The Martian",
        "author": "Andy Weir",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book06":{
        "book_id": "Book06",
        "title": "Silent Spring",
        "author": "Rachel Carson",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book07":{
        "book_id": "Book07",
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book08":{
        "book_id": "Book08",
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book09":{
        "book_id": "Book09",
        "title": "Into Thin Air",
        "author": "Jon Krakauer",
        "available" : True,
        "borrower_id": None, 
    },    
    
    "Book10":{
        "book_id": "Book10",
        "title": "Born a Crime",
        "author": "Trevor Noah",
        "available" : True,
        "borrower_id": None, 
    },
}

# Lock so only one borrow or return can change the inventory at a time.
lock = threading.Lock()

# RPyC service exposing the library's remote procedure to clients.
class LibraryListService(rpyc.Service):

    # Logs a message when a client connects.
    def on_connect(self, connection):

        print("A client has connected.")

    # Logs a message when a client disconnects.
    def on_disconnect(self, connection):

        print("A client has disconnected.")

    # Returns copies of every book record in the library
    def exposed_get_all_books(self):
        books = []
        for book in library.values():
            books.append(book.copy())

        return {
            "success": True,
            "message": f"Found {len(books)} books.",
            "data" : books,
        }

    # Returns books whose title, athor, or ID contains the keyword (case-insensitive)
    def exposed_search_book(self, keyword):
        keyword = keyword.strip().lower()

        if not keyword:
            return {
                "success": False,
                "message": "Please enter a keyword to start search.",
                "data" : None,
            }

        matches = []
        for book in library.values():
            if (keyword in book["title"].lower() 
                    or keyword in book["author"].lower()
                    or keyword in book["book_id"].lower()):
                matches.append(book.copy())
        
        return {
            "success": True,
            "message": f"Matches found: {len(matches)}.",
            "data" : matches,
        }

    # Reports whether the given book exists and is available to borrow
    def exposed_check_availability(self, book_id):
        book_id = book_id.strip().capitalize()

        if book_id not in library:
           return {
                "success": False,
                "message": f"{book_id} does not exist.",
                "data" : None,
        }
    
        book = library[book_id]

        if book["available"]:
            message = f"{book_id} is available."
        else:
            message = f"{book_id} is not available."

        return {
            "success": True,
            "message": message,
            "data" : book.copy(),
        }

    # Private helper: checks that a student ID matches the format S#### (not callable by clients)
    def is_valid_student_id(self, student_id):
        return (len(student_id) == 5
                and student_id.startswith("S")
                and student_id[1:].isdigit())

    # Returns all books currently checked out to the given student.
    def exposed_get_borrowed_books(self, student_id):
        student_id = student_id.strip().upper()

        if not self.is_valid_student_id(student_id):
           return {
                "success": False,
                "message": f"{student_id} is not a valid student ID. Expected format: 'S1001'.",
                "data" : None,
        }

        borrowed_books = []
        
        for book in library.values():
            if book["borrower_id"] == student_id:
                borrowed_books.append(book.copy())
            
        return {
            "success": True,
            "message": f"Student {student_id} has {len(borrowed_books)} books checked out.",
            "data" : borrowed_books,
        }

    # Checks out an available book to a valid student, holding the lock during the update.
    def exposed_borrow_book(self, student_id, book_id):
        student_id = student_id.strip().upper()
        book_id = book_id.strip().capitalize()

        if not self.is_valid_student_id(student_id):
           return {
                "success": False,
                "message": f"{student_id} is not a valid student ID. Expected format: 'S1001'.",
                "data" : None,
        }

        with lock:

            if book_id not in library:
                return {
                    "success": False,
                    "message": f"{book_id} does not exist.",
                    "data" : None,
                }

            book = library[book_id]

            if not book["available"]:
                return {
                    "success": False,
                    "message": f"{book_id} is currently unavailable.",
                    "data": None,
                }

            book["available"] = False
            book["borrower_id"] = student_id

            return {
                "success": True,
                "message": f"{book_id} checked out to {student_id}.",
                "data": book.copy(),
            }

    # Returns a book only if it is checked out by this student, holding the lock during the update.
    def exposed_return_book(self, student_id, book_id):
        student_id = student_id.strip().upper()
        book_id = book_id.strip().capitalize()

        if not self.is_valid_student_id(student_id):
           return {
                "success": False,
                "message": f"{student_id} is not a valid student ID. Expected format: 'S1001'.",
                "data" : None,
        }

        with lock:

            if book_id not in library:
                return {
                    "success": False,
                    "message": f"{book_id} does not exist.",
                    "data" : None,
                }

            book = library[book_id]

            if book["available"]:
                return {
                    "success": False,
                    "message": f"{book_id} is currently not checked out.",
                    "data": None,
                }

            if book["borrower_id"] != student_id:
                return {
                    "success": False,
                    "message": f"{book_id} was not borrowed by {student_id}.",
                    "data": None,
                }

            book["available"] = True
            book["borrower_id"] = None

            return {
                "success": True,
                "message": f"Student {student_id} returned {book_id}.",
                "data": book.copy(),
            }

# Creates the threaded RPC srver and starts listening for client requests.
def main():

    server = ThreadedServer(
        LibraryListService,

        hostname=SERVER,

        port=PORT,

        protocol_config={"allow_public_attrs": True}
    )

    print(f"Library server is running on {SERVER}:{PORT}")

    print("Press Ctrl+C to stop the server.")

    server.start()

if __name__ == "__main__":

    main()





