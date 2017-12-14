class Storage:
    def __init__(self, recipientName, lockerId, dateofdelivery, phonenumber, emailaddress):
        self.__recipientName = recipientName
        self.__lockerId = lockerId
        self.__dateofdelivery = dateofdelivery
        self.__phonenumber = phonenumber
        self.__emailaddress = emailaddress

    def get_recipientName(self):
        return self.__recipientName

    def get_lockerId(self):
        return self.__lockerId

    def get_dateofdelivery(self):
        return self.__dateofdelivery

    def get_phonenumber(self):
        return self.__phonenumber

    def get_emailaddress(self):
        return self.__emailaddress

    def set_recipientName(self, recipientName):
        self.__recipientName = recipientName

    def set_lockerId(self, lockerId):
        self.__lockerId = lockerId

    def set_dateofdelivery(self, dateofdelivery):
        self.__dateofdelivery = dateofdelivery

    def set_phonenumber(self, phonenumber):
        self.__phonenumber = phonenumber

    def set_emailaddress(self, emailaddress):
        self.__emailaddress = emailaddress
