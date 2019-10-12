from src.core.database.user import User


class Book:
    def __init__(self, name, author, renter: User, rented_at):
        self.name = name
        self.author = author
        self.renter = renter
        self.rented_at = rented_at
