
from .Users import Users

class Customer(Users):
    def __init__(self, username, password, phone_no, email, address):
        Users.__init__(self, username, password, phone_no, email)
        self.__address = address

    def get_addresss(self):
        return self.__address

    def set_address(self, address):
        self.__address = address
