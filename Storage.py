class Storage:
    def __init__(self, recipientName, blocknumber, unitnumber):
        self.__recipientName = recipientName
        self.__blocknumber = blocknumber
        self.__unitnumber = unitnumber

    def get_recipientName(self):
        return self.__recipientName

    def get_blocknumber(self):
        return self.__blocknumber

    def get_unitnumber(self):
        return self.__unitnumber

    def set_recipientName(self, recipientName):
        self.__recipientName = recipientName

    def set_blocknumber(self, blocknumber):
        self.__blocknumber = blocknumber

    def set_unitnumber(self, unitnumber):
        self.__unitnumber = unitnumber


class customer(Storage):
    def __init__(self,recipientName,unitnumber,blocknumber):
        super().__init__(recipientName,unitnumber,blocknumber)
        self.__blocknumber = blocknumber
        self.__unitnumber = unitnumber
    def get_unitnumber(self):
        return self.__unitnumber
    def get_blocknumber(self):
        return self.__blocknumber

    def set_emailaddress(self, emailaddress):
        self.__emailaddress = emailaddress
    def set_blocknumber(self, blocknumber):
        self.__blocknumber = blocknumber


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

