import Screen_manager


class Help_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if Help_screen.__instance == None:
            Help_screen()
        return Help_screen.__instance

    def __init__(self):
        if Help_screen.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("Help_screen class is singleton")
        else:

            # TODO

            Help_screen.__instance = self


    def go_to_help_screen(self):
        # TODO
        pass