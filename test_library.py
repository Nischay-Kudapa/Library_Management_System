from lms import *

# Create an address
address = Address("123 Street", "CityName", "StateName", "123456", "Country")

# Create a librarian and a member
librarian = Librarian("lib123", "pass123", Person("John Doe", address, "john@example.com", "9876543210"))
member = Member("mem001", "pass456", Person("Jane Doe", address, "jane@example.com", "9876543211"))

# Create a book item
book_item = BookItem(
    ISBN="978-3-16-148410-0",
    title="Python Programming",
    subject="Computer Science",
    publisher="TechPress",
    language="English",
    number_of_pages=500,
    barcode="PY123456",
    is_reference_only=False,
    price=299.99,
    book_format=BookFormat.HARDCOVER,
    status=BookStatus.AVAILABLE,
    date_of_purchase=datetime.today(),
    publication_date=datetime(2020, 5, 1),
    placed_at=Rack(1, "A1")
)

# Librarian adds the book to the library
librarian.add_book_item(book_item)

# Member tries to checkout the book
if member.checkout_book_item(book_item):
    print("Book checked out successfully!")
else:
    print("Book checkout failed.")

# Member returns the book
member.return_book_item(book_item)
print(f"Book {book_item.title} returned.")

