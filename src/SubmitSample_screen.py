

class SubmitSample_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if SubmitSample_screen.__instance == None:
            SubmitSample_screen()
        return SubmitSample_screen.__instance

    def __init__(self):
        if SubmitSample_screen.__instance != None:
            raise Exception("SubmitSample_screen class is singleton")
        else:

            # TODO

            SubmitSample_screen.__instance = self


    def go_to_submitSample_screen(self):
        # TODO
        pass