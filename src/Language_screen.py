
import Screen_manager

class Language_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if Language_screen.__instance == None:
            Language_screen()
        return Language_screen.__instance

    def __init__(self):
        if Language_screen.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("Language_screen class is singleton")
        else:

            # TODO

            Language_screen.__instance = self


    def go_to_language_screen(self):
        # TODO
        pass