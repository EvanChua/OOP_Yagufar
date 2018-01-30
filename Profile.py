class Profile:
    def __init__(self,phone_number, email_address, profile_pic, profile_desc):
        self.__profileid = ""

        self.__phone_number = phone_number
        self.__email_address = email_address
        self.__profile_pic = profile_pic
        self.__profile_desc = profile_desc

    def get_profileid(self):
        return self.__profileid

    def set_profileid(self, profileid):
        self.__profileid = profileid



    def get_phone_number(self):
        return self.__phone_number
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_email_address(self):
        return self.__email_address
    def set_email_address(self, email_address):
        self.__email_address = email_address

    def get_profile_pic(self):
        return self.__profile_pic

    def set_profile_pic(self, profile_pic):
        self.__profile_pic = profile_pic

    def get_profile_desc(self):
        return self.__profile_desc

    def set_profile_desc(self, profile_desc):
        self.__profile_desc = profile_desc



