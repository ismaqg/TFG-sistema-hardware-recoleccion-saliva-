from tkinter import *

from PIL import ImageTk,Image
import constants
import Screen_manager
import Checker
from Not_available import Not_available
from LogIn_screen import LogIn_screen


class Screen_saver():  # singleton

    __instance = None

    @staticmethod 
    def getInstance():
        if Screen_saver.__instance == None:
            Screen_saver()
        return Screen_saver.__instance

    def __init__(self):
        if Screen_saver.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("Screen_saver class is singleton")
        else:
            self.__inactivity_countdown = None  # Identifies the inactivity countdown to check if all the resources are available (specially if hardware is responding)

            self.__screen_saver_frame = Screen_manager.init_screen_frame()

            img = Image.open(constants.IMAGES_DIRECTORY + "screensaver.png")
            img = img.resize((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), Image.ANTIALIAS)
            self.__saver_img = ImageTk.PhotoImage( img )  # saver_img needs to be a class atribute. Otherwise, it won't work
            wake_up_button = Button(self.__screen_saver_frame, image = self.__saver_img , command = self.__user_interaction)
            wake_up_button.grid(row=0, column=0, sticky='NSEW')

            Screen_saver.__instance = self

    def __user_interaction(self):
        Screen_manager.get_root().after_cancel(self.__inactivity_countdown)
        LogIn_screen.getInstance().go_to_login_screen()

    def __inactivity_timeout(self):
        available = Checker.check_available_resources()
        if available:
            self.__inactivity_countdown = Screen_manager.get_root().after(constants.INACTIVITY_CHECK_RESOURCES_TIMER, self.__inactivity_timeout)
        else:  # The operator has been warned on the previous function and the info_uso DB has been updated with this error
            Not_available.getInstance().go_to_not_available_screen()

    def go_to_screen_saver(self):
        self.__inactivity_countdown = Screen_manager.get_root().after(constants.INACTIVITY_CHECK_RESOURCES_TIMER, self.__inactivity_timeout)
        LogIn_screen.getInstance().set_login_screen_isActive(False)
        self.__screen_saver_frame.tkraise()
         