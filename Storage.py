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
    def __init__(self,recipientName,blocknumber,unitnumber):
        super().__init__(recipientName,blocknumber,unitnumber )
        self.__blocknumber = blocknumber
        self.__unitnumber = unitnumber
    def get_unitnumber(self):
        return self.__unitnumber
    def get_blocknumber(self):
        return self.__blocknumber
    def get_info(self):
        return self.__info
    # def get_id(self):
    #     return self.__id

    def set_unitnumber(self, unitnumber):
        self.__unitnumber = unitnumber
    def set_blocknumber(self, blocknumber):
        self.__blocknumber = blocknumber
    def set_info(self,info):
        self.__info = info
    # def set_id(self, id):
    #     self.__id = id


class deliveryman(Storage):
    def __init__(self, recipientName,lockerId, dateofdelivery, id):
        super().__init__(recipientName, lockerId, dateofdelivery)
        self.__lockerId = lockerId
        self.__dateofdelivery = dateofdelivery
        self.__id = id

    def get_lockerId(self):
        return self.__lockerId
    def get_dateofdelivery(self):
        return self.__dateofdelivery
    def get_info2(self):
        return self.__info2
    def get_id(self):
        return self.__id


    def set_lockerId(self, lockerId):
        self.__lockerId = lockerId
    def set_dateofdelivery(self, dateofdelivery):
        self.__dateofdelivery = dateofdelivery
    def set_info2(self,info2):
        self.__info2 = info2
    def set_id(self, id):
        self.__id = id




