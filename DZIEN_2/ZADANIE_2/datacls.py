from dataclasses import dataclass
from typing import Optional

class Author:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    def __repr__(self):
        return f"Author: {self.first_name} {self.last_name}"

@dataclass
class Book:
    title: str
    author: Author
    price: float
    isbn: Optional[str] = None

b1 = Book("The Hobbit", Author("John","Tolkien"), 39.95,"63455345345")
b2 = Book("Wiedźmin", "Andrzej Sapkowski", 51.99,"986787534523")
b3 = Book("Czarna Wieża", "Steven King", 66.8)

print(b1)
print(b2)
print(b3)
print(b1.isbn, b1.title)
print(b2.isbn,  b2.title)
print(b3.isbn,  b3.title)

print("________________________________________")


a1 = Author("John", "Tolkien")
a2 = Author("Andrzej", "Sapkowski")
a3 = Author("Steven", "King")
print(a1)
print(a2)
print(a3)

