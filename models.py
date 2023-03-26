from typing import Dict, List

class UserModel:

    def __init__(self, name, email):
        self.name = name
        self.likes = email

    def to_dict(self) -> Dict:
        return self.__dict__


class BookModel:

    def __init__(self, id, name, book_price):
        self.id = id
        self.name = name
        self.book_price = book_price

    def to_dict(self) -> Dict:
        return self.__dict__

