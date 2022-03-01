
from tkinter import *

from PIL import ImageTk,Image
import Screen_manager
import constants
import Language_controller
from Language_controller import Language

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

            self.__languageScreen_frame = Screen_manager.init_screen_frame()

            img_spanish = Image.open(constants.IMAGES_DIRECTORY + "spanish.png")
            img_catalan = Image.open(constants.IMAGES_DIRECTORY + "catalan.png")
            img_english = Image.open(constants.IMAGES_DIRECTORY + "english.png")
            img_spanish = img_spanish.resize((int(constants.SCREEN_WIDTH/3 - 20), int(constants.SCREEN_HEIGHT/2)), Image.ANTIALIAS)
            img_catalan = img_catalan.resize((int(constants.SCREEN_WIDTH/3 - 20), int(constants.SCREEN_HEIGHT/2)), Image.ANTIALIAS)
            img_english = img_english.resize((int(constants.SCREEN_WIDTH/3 - 20), int(constants.SCREEN_HEIGHT/2)), Image.ANTIALIAS)
            self.__img_spanish = ImageTk.PhotoImage( img_spanish )  # the images that we are going to use in the buttons need to be class atributes. Otherwise, it won't work
            self.__img_catalan = ImageTk.PhotoImage( img_catalan )
            self.__img_english = ImageTk.PhotoImage( img_english )

            self.__spanish_b = Button(self.__languageScreen_frame, image = self.__img_spanish, command=lambda:self.__change_language(Language.SPANISH))
            self.__catalan_b = Button(self.__languageScreen_frame, image = self.__img_catalan, command=lambda:self.__change_language(Language.CATALAN))
            self.__english_b = Button(self.__languageScreen_frame, image = self.__img_english, command=lambda:self.__change_language(Language.ENGLISH))

            self.__spanish_b.grid(row = 0, column = 0, sticky = 'NSEW', pady = constants.SCREEN_HEIGHT/4, padx = (20, 10)) 
            self.__catalan_b.grid(row = 0, column = 1, sticky = 'NSEW', pady = constants.SCREEN_HEIGHT/4, padx = 10)
            self.__english_b.grid(row = 0, column = 2, sticky = 'NSEW', pady = constants.SCREEN_HEIGHT/4, padx = (10, 20))

            self.__languageScreen_frame.rowconfigure(0, weight=1)
            self.__languageScreen_frame.columnconfigure(0, weight=1)
            self.__languageScreen_frame.columnconfigure(1, weight=1)
            self.__languageScreen_frame.columnconfigure(2, weight=1)

            Language_screen.__instance = self


    def __change_language(self, language):
        Language_controller.set_current_language(language)
        # Once one language has been selected, the system returns to the previous scene (LogIn screen):
        from LogIn_screen import LogIn_screen  # here to avoid circular dependency
        LogIn_screen.getInstance().go_to_login_screen()

    def go_to_language_screen(self):
        from LogIn_screen import LogIn_screen  # here to avoid circular dependency
        LogIn_screen.getInstance().set_login_screen_isActive(False)
        self.__languageScreen_frame.tkraise()