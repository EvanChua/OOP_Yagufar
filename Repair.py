class Repair:
    def __init__(self, date, time, quest):
        self.__chooseDate = date
        self.__chooseTime = time
        self.__chooseQuest = quest

    def get_chooseDate(self):
        return self.__chooseDate

    def get_chooseTime(self):
        return self.__chooseTime

    def get_chooseQuest(self):
        return self.__chooseQuest

    def set_chooseDate(self, date):
        self.__chooseDate = date

    def set_chooseTime(self, time):
        self.__chooseTime = time

    def set_chooseQuest(self, quest):
        self.__chooseQuest = quest
