class Users:
    def __init__(self, username, password, phone_number, email_address):
        self.__profileid = ""
        self.__username = username
        self.__password = password
        self.__phone_number = phone_number
        self.__email_address = email_address

    def get_profileid(self):
        return self.__profileid

    def set_profileid(self, profileid):
        self.__profileid = profileid

    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password
    def set_password(self, password):
        self.__password = password

    def get_phone_number(self):
        return self.__phone_number
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_email_address(self):
        return self.__email_address
    def set_email_address(self, email_address):
        self.__email_address = email_address

# class Customer(Users):
#     def __init__(self, username, password, phone_no, email, address):
#         Users.__init__(self, username, password, phone_no, email)
#         self.__address = address
#
#     def get_addresss(self):
#         return self.__address
#
#     def set_address(self, address):
#         self.__address = address
#
# class technician(Users):
#     def __init__(self, username, password, phone_no, email, occupation, company_name):
#         Users.__init__(self, username, password, phone_no, email)
#         self.__occupation = occupation
#         self.__company_name = company_name
#
#     def get_occupation(self):
#         return self.__occupation
#
#     def set_occupation(self, occupation):
#         self.__occupation = occupation
#
#     def get_company_name(self):
#         return self.__company_name
#
#     def set_company_name(self, company_name):
#         self.__company_name = company_name
