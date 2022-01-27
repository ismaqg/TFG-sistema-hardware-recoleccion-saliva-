from matplotlib.pyplot import summer
from MainScreen import MainScreen


class MainScreen_user(MainScreen):  # singleton 

    __instance = None

    @staticmethod
    def getInstance():
        if MainScreen_user.__instance == None:
            MainScreen_user()
        return MainScreen_user.__instance

    def __init__(self):
        if MainScreen_user.__instance != None:
            raise Exception("MainScreen_admin class is singleton")
        else:
            super().create_main_frames()

            # TODO: Declaro los botones y tal pero NO hago el .grid. El .grid lo pongo en el "go to main screen" antes del tk_raise

            MainScreen_user.__instance = self


    # override parent method
    def go_to_main_screen(self):
        # TODO: Los .grid y luego el tk_raise
        pass

    # override parent method
    def _erase_mainScreen_contents(self):
        # TODO: Los .gridforget. Si da error algo de quí es que se debe llamar _erase_mainScreen_contents en lugar de con __ delante. También tendría que cambiar la llamada de la funcion logOut
        pass

    def logOut(self):
        self._erase_mainScreen_contents()
        super().logOut()
        pass