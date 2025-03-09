from abc import ABC
from enum import Enum, auto
from datetime import datetime, timedelta


class BookFormat(Enum):
    HARDCOVER = auto()
    PAPERBACK = auto()
    AUDIO_BOOK = auto()
    EBOOK = auto()
    NEWSPAPER = auto()
    MAGAZINE = auto()
    JOURNAL = auto()


class BookStatus(Enum):
    AVAILABLE = auto()
    RESERVED = auto()
    LOANED = auto()
    LOST = auto()


class ReservationStatus(Enum):
    WAITING = auto()
    PENDING = auto()
    CANCELED = auto()
    NONE = auto()
    COMPLETED = auto()


class AccountStatus(Enum):
    ACTIVE = auto()
    CLOSED = auto()
    CANCELED = auto()
    BLACKLISTED = auto()
    NONE = auto()


class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.street_address = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country


class Person(ABC):
    def __init__(self, name, address, email, phone):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone


class Constants:
    MAX_BOOKS_ISSUED_TO_A_USER = 5
    MAX_LENDING_DAYS = 10


class Account(ABC):
    def __init__(self, id, password, person, status=AccountStatus.ACTIVE):
        self.id = id
        self.password = password
        self.status = status
        self.person = person

    def reset_password(self, new_password):
        self.password = new_password
        print("Password reset successfully.")


class Librarian(Account):
    def add_book_item(self, book_item):
        print(f"Book {book_item.barcode} added to the library.")

    def block_member(self, member):
        member.status = AccountStatus.BLACKLISTED
        print(f"Member {member.id} is blocked.")

    def unblock_member(self, member):
        member.status = AccountStatus.ACTIVE
        print(f"Member {member.id} is unblocked.")


class Member(Account):
    def __init__(self, id, password, person, status=AccountStatus.ACTIVE):
        super().__init__(id, password, person, status)
        self.date_of_membership = datetime.today()
        self.total_books_checkedout = 0
        self.constants = Constants()

    def get_total_books_checkedout(self):
        return self.total_books_checkedout

    def increment_total_books_checkedout(self):
        self.total_books_checkedout += 1

    def decrement_total_books_checkedout(self):
        if self.total_books_checkedout > 0:
            self.total_books_checkedout -= 1

    def checkout_book_item(self, book_item):
        if self.get_total_books_checkedout() >= self.constants.MAX_BOOKS_ISSUED_TO_A_USER:
            print("Maximum book limit reached.")
            return False

        book_reservation = BookReservation.fetch_reservation_details(book_item.barcode)
        if book_reservation and book_reservation.member_id != self.id:
            print("Book is reserved by another member.")
            return False
        elif book_reservation:
            book_reservation.update_status(ReservationStatus.COMPLETED)

        if not book_item.checkout(self.id):
            return False

        self.increment_total_books_checkedout()
        return True

    def check_for_fine(self, book_item_barcode):
        book_lending = BookLending.fetch_lending_details(book_item_barcode)
        if book_lending:
            due_date = book_lending.due_date
            if datetime.today() > due_date:
                overdue_days = (datetime.today() - due_date).days
                Fine.collect_fine(self.id, overdue_days)

    def return_book_item(self, book_item):
        self.check_for_fine(book_item.barcode)
        book_reservation = BookReservation.fetch_reservation_details(book_item.barcode)
        if book_reservation:
            book_item.update_book_item_status(BookStatus.RESERVED)
            book_reservation.send_book_available_notification()
        book_item.update_book_item_status(BookStatus.AVAILABLE)


class BookReservation:
    def __init__(self, creation_date, status, book_item_barcode, member_id):
        self.creation_date = creation_date
        self.status = status
        self.book_item_barcode = book_item_barcode
        self.member_id = member_id

    @staticmethod
    def fetch_reservation_details(barcode):
        return None

    def update_status(self, status):
        self.status = status


class BookLending:
    def __init__(self, creation_date, due_date, book_item_barcode, member_id):
        self.creation_date = creation_date
        self.due_date = due_date
        self.return_date = None
        self.book_item_barcode = book_item_barcode
        self.member_id = member_id

    @staticmethod
    def lend_book(barcode, member_id):
        return True

    @staticmethod
    def fetch_lending_details(barcode):
        return None


class Fine:
    @staticmethod
    def collect_fine(member_id, days):
        print(f"Fine collected from member {member_id} for {days} overdue days.")


class Book(ABC):
    def __init__(self, ISBN, title, subject, publisher, language, number_of_pages):
        self.ISBN = ISBN
        self.title = title
        self.subject = subject
        self.publisher = publisher
        self.language = language
        self.number_of_pages = number_of_pages
        self.authors = []


class BookItem(Book):
    def __init__(self, ISBN, title, subject, publisher, language, number_of_pages,
                 barcode, is_reference_only, price, book_format, status, date_of_purchase, publication_date, placed_at):
        super().__init__(ISBN, title, subject, publisher, language, number_of_pages)
        self.barcode = barcode
        self.is_reference_only = is_reference_only
        self.price = price
        self.format = book_format
        self.status = status
        self.date_of_purchase = date_of_purchase
        self.publication_date = publication_date
        self.placed_at = placed_at

    def checkout(self, member_id):
        if self.is_reference_only:
            print("This book is reference-only and cannot be checked out.")
            return False
        if not BookLending.lend_book(self.barcode, member_id):
            return False
        self.status = BookStatus.LOANED
        return True

    def update_book_item_status(self, status):
        self.status = status


class Rack:
    def __init__(self, number, location_identifier):
        self.number = number
        self.location_identifier = location_identifier


class Search(ABC):
    def search_by_title(self, title):
        return None

    def search_by_author(self, author):
        return None

    def search_by_subject(self, subject):
        return None

    def search_by_pub_date(self, publish_date):
        return None


class Catalog(Search):
    def __init__(self):
        self.book_titles = {}
        self.book_authors = {}
        self.book_subjects = {}
        self.book_publication_dates = {}

    def search_by_title(self, query):
        return self.book_titles.get(query)

    def search_by_author(self, query):
        return self.book_authors.get(query)
