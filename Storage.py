class Storage:
    def __init__(self, recipientName, phonenumber, emailaddress):
        self.__recipientName = recipientName
        self.__phonenumber = phonenumber
        self.__emailaddress = emailaddress

    def get_recipientName(self):
        return self.__recipientName

    def get_phonenumber(self):
        return self.__phonenumber

    def get_emailaddress(self):
        return self.__emailaddress

    def set_recipientName(self, recipientName):
        self.__recipientName = recipientName

    def set_phonenumber(self, phonenumber):
        self.__phonenumber = phonenumber

    def set_emailaddress(self, emailaddress):
        self.__emailaddress = emailaddress

class customer(Storage):
    def __init__(self,recipientName,emailaddress,phonenumber):
        super().__init__(recipientName,emailaddress,phonenumber)
        self.__phonenumber = phonenumber
        self.__emailaddress = emailaddress
    def get_emailaddress(self):
        return self.__emailaddress
    def get_phonenumber(self):
        return self.__phonenumber

    def set_emailaddress(self, emailaddress):
        self.__emailaddress = emailaddress
    def set_phonenumber(self, phonenumber):
        self.__phonenumber = phonenumber


class deliveryman(Storage):
    def __init__(self, recipientName,lockerId, dateofdelivery):
        super().__init__(recipientName, lockerId, dateofdelivery)
        self.__lockerId = lockerId
        self.__dateofdelivery = dateofdelivery
    def get_lockerId(self):
        return self.__lockerId
    def get_dateofdelivery(self):
        return self.__dateofdelivery

    def set_lockerId(self, lockerId):
        self.__lockerId = lockerId
    def set_dateofdelivery(self, dateofdelivery):
        self.__dateofdelivery = dateofdelivery

