class Users:
    def __init__(self, username,name ,password, phone_number, email_address, block, unit ,  profile_pic, profile_desc, type):
        self.__profileid = ""
        self.__username = username
        self.__name = name
        self.__password = password
        self.__phone_number = phone_number
        self.__email_address = email_address
        self.__block = block
        self.__unit = unit
        self.__profile_pic = profile_pic
        self.__profile_desc = profile_desc
        self.__type = type

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

    def get_block(self):
        return self.__block
    def set_block(self, block):
        self.__block = block

    def get_unit(self):
        return self.__unit
    def set_unit(self, unit):
        self.__unit = unit

    def get_type(self):
        return self.__type
    def set_type(self, type):
        self.__type = type

    def get_profile_pic(self):
        return self.__profile_pic

    def set_profile_pic(self, profile_pic):
        self.__profile_pic = profile_pic

    def get_profile_desc(self):
        return self.__profile_desc

    def set_profile_desc(self, profile_desc):
        self.__profile_desc = profile_desc



