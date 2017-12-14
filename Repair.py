class Repair:
    def __init__(self, service, location, quest):
        self.__chooseService = service
        self.__chooseLocation = location
        self.__chooseQuest = quest

    def get_chooseService(self):
        return self.__chooseService

    def get_chooseLocation(self):
        return self.__chooseLocation

    def get_chooseQuest(self):
        return self.__chooseQuest

    def set_chooseService(self, service):
        self.__chooseService = service

    def set_chooseLocation(self, location):
        self.__chooseLocation = location

    def set_chooseQuest(self, quest):
        self.__chooseQuest = quest