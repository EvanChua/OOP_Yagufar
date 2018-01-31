class Profile:
    def __init__(self, profile_pic, profile_desc):
        self.__profile_pic = profile_pic
        self.__profile_desc = profile_desc

    def get_profile_pic(self):
        return self.__profile_pic

    def set_profile_pic(self, profile_pic):
        self.__profile_pic = profile_pic

    def get_profile_desc(self):
        return self.__profile_desc

    def set_profile_desc(self, profile_desc):
        self.__profile_desc = profile_desc
