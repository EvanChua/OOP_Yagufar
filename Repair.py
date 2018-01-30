class Repair:
    def __init__(self, service, location, date, time, quest):
        self.__chooseService = service
        self.__chooseLocation = location
        self.__chooseDate = date
        self.__chooseTime = time
        self.__chooseQuest = quest

    def get_chooseService(self):
        return self.__chooseService

    def get_chooseLocation(self):
        return self.__chooseLocation

    def get_chooseDate(self):
        return self.__chooseDate

    def get_chooseTime(self):
        return self.__chooseTime

    def get_chooseQuest(self):
        return self.__chooseQuest

    def set_chooseService(self, service):
        self.__chooseService = service

    def set_chooseLocation(self, location):
        self.__chooseLocation = location

    def set_chooseDate(self, date):
        self.__chooseDate = date

    def set_chooseTime(self, time):
        self.__chooseTime = time

    def set_chooseQuest(self, quest):
        self.__chooseQuest = quest
