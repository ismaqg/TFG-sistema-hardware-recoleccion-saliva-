import DBcontroller

class Person:
    def __init__(self, CIP):
        self.__CIP = CIP
        admins = DBcontroller.get_admins()
        operators = DBcontroller.get_operators()
        if CIP in admins:
            self.__status = "Admin"
        elif CIP in operators:
            self.__status = "Operator"
        else:
            self.__status = "User"

    def get_status(self):
        return self.__status

    def get_CIP(self):
        return self.__CIP
