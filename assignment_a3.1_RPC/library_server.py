import threading

import rpyc

from rpyc.utils.server import ThreadedServer



SERVER = "localhost"

PORT = 18861

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

threading.Lock()

class LibraryListService(rpyc.Service):

    def on_connect(self, connection):

        print("A client has connected.")

    def on_disconnect(self, connection):

        print("A client has disconnected.")

    def exposed_append(self, data):

        self.value.append(data)

        print(f"Appended value: {data}")

        return list(self.value)

    def exposed_get_value(self):

        return list(self.value)

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





