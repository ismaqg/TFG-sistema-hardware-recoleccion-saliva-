from ast import Raise
import DBcontroller

# TODO: Probablemente necesitara ser singleton a modo de unico "activeUser"

# Represents de active user / operator / admin using the machine
# Login will use the constructor and the rest of the classes, when need to consult the current active person, will use the getCurrent method.
# Logout will need to forget the current active person. Also, Login will need to do that if a new active person has been created but finally has not accessed the system
class ActivePerson:

    __instance = None

    @staticmethod
    def getCurrent():
        if ActivePerson.__instance == None:
            raise Exception("There is not a user / admin / operator using right now the system")
        else:
            return ActivePerson.__instance

    @staticmethod
    def destroyCurrent():
        ActivePerson.__instance = None

    @staticmethod
    def isActivePerson():
        if ActivePerson.__instance == None:
            return False
        else:
            return True

    def __init__(self, CIP):
        if ActivePerson.__instance != None:
            raise Exception("There is someone using the system right now")
        else:
            self.__CIP = CIP
            admins = DBcontroller.get_admins()
            operators = DBcontroller.get_operators()
            if CIP in admins:
                self.__status = "ADMIN"
            elif CIP in operators:
                self.__status = "OPERATOR"
            else:
                self.__status = "USER"
            ActivePerson.__instance = self

     

    def get_status(self):
        return self.__status

    def get_CIP(self):
        return self.__CIP
