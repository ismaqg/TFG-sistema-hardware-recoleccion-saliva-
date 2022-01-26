from MainScreen import MainScreen


class MainScreen_admin(MainScreen):  # singleton 

    __instance = None

    @staticmethod
    def getInstance():
        if MainScreen_admin.__instance == None:
            MainScreen_admin()
        return MainScreen_admin.__instance

    def __init__(self):
        if MainScreen_admin.__instance != None:
            raise Exception("MainScreen_admin class is singleton")
        else:
            super().create_main_frame()

            # TODO: Declaro los botones y tal pero NO hago el .grid. El .grid lo pongo en el "go to main screen" antes del tk_raise

            MainScreen_admin.__instance = self


    # override parent method
    def go_to_main_screen(self):
        # TODO: Los .grid y luego el tk_raise
        pass

    # override parent method
    def logOut(self):
        # TODO: grid forget + logout base datos + LogIn_Screen.go_to_login_screen()
        pass