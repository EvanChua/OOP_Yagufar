
class technician:
    def __init__(self, username , name, password, phone_number, email_address , postal , occupation, companyname, type):
        self.__profileid = ""
        self.__username = username
        self.__name = name
        self.__password = password
        self.__phone_number = phone_number
        self.__email_address = email_address
        self.__postal = postal
        self.__occupation = occupation
        self.__companyname = companyname
        self.__type = type

    def get_occupation(self):
        return self.__occupation
    def set_occupation(self, occupation):
        self.__occupation = occupation

    def get_companyname(self):
        return self.__companyname
    def set_companyname(self, companyname):
        self.__companyname = companyname

    def get_profileid(self):
        return self.__profileid
    def set_profileid(self, profileid):
        self.__profileid = profileid

    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_name(self):
        return self.__name
    def set_username(self, name):
        self.__name = name

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

    def get_postal(self):
        return self.__postal
    def set_postal(self, postal):
        self.__postal = postal

    def get_type(self):
        return self.__type
    def set_Type(self, type):
        self.__type = type
