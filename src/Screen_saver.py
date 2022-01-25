from tkinter import *

from PIL import ImageTk,Image
import constants
import Screen_manager
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
            raise Exception("Screen_saver class is singleton")
        else:
            self.__screen_saver_frame = Screen_manager.init_screen_frame()

            img = Image.open(constants.IMAGES_DIRECTORY + "screensaver.png")
            img = img.resize((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), Image.ANTIALIAS)
            self.__saver_img = ImageTk.PhotoImage( img )
            wake_up_button = Button(self.__screen_saver_frame, image = self.__saver_img , command = LogIn_screen.getInstance().go_to_login_screen)
            wake_up_button.grid(row=0,column=0,sticky='NSEW')

            Screen_saver.__instance = self


    def go_to_screen_saver(self):
        self.__screen_saver_frame.tkraise()
        LogIn_screen.getInstance().set_login_screen_isActive(False) 