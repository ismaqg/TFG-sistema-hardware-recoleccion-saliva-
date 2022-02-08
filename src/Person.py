import DBcontroller


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
    def isThereActivePerson():
        if ActivePerson.__instance == None:
            return False
        else:
            return True


    def __init__(self, CIP):
        if ActivePerson.__instance != None:
            raise Exception("There is someone using the system right now")
        else:
            self.__user_has_submitted_in_this_session = False
            self.__user_has_claimed_kit_in_this_session = False
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


    def logOut(self):
        if ActivePerson.__instance == None:
            raise Exception("There is not a user / admin / operator using right now the system")
        else:
            DBcontroller.add_new_event(self.get_CIP(), self.get_status() + " LOGOUT")
            from LogIn_screen import LogIn_screen  # Declared here to avoid circular dependency
            from MainScreen_user import MainScreen_user
            from MainScreen_admin import MainScreen_admin
            from MainScreen_operator import MainScreen_operator
            MainScreen_user.getInstance().erase_mainScreen_contents()
            MainScreen_admin.getInstance().erase_mainScreen_contents()
            MainScreen_operator.getInstance().erase_mainScreen_contents()
            ActivePerson.destroyCurrent()  # here and not before because the getInstance() of the 3 previous lines creates an instance if not exists, and to create the instance is called the ActivePerson.getCurrent(), which throws an exception if the current active user has been destroyed
            LogIn_screen.getInstance().go_to_login_screen()
     

    def get_status(self):
        return self.__status

    def get_CIP(self):
        return self.__CIP

    def get_has_submitted_in_this_session(self):
        if self.__status != "USER":
            raise Exception("current person using the system is not a user")
        return self.__user_has_submitted_in_this_session

    def set_has_submitted_to_true(self):
        if self.__status != "USER":
            raise Exception("current person using the system is not a user")
        self.__user_has_submitted_in_this_session = True

    def get_has_claimed_kit_in_this_session(self):
        if self.__status != "USER":
            raise Exception("current person using the system is not a user")
        return self.__user_has_claimed_kit_in_this_session

    def set_has_claimed_kit_to_true(self):
        if self.__status != "USER":
            raise Exception("current person using the system is not a user")
        self.__user_has_claimed_kit_in_this_session = True
