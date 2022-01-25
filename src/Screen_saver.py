from tkinter import *

from PIL import ImageTk,Image
import constants
import Screen_manager
from LogIn_screen import LogIn_screen

class Screen_saver():

    def __init__(self):
        self.__screen_saver_frame = Screen_manager.init_screen_frame()

        img = Image.open(constants.IMAGES_DIRECTORY + "screensaver.png")
        img = img.resize((Screen_manager.get_root().winfo_screenwidth(), Screen_manager.get_root().winfo_screenheight()), Image.ANTIALIAS)
        self.__saver_img = ImageTk.PhotoImage( img )
        wake_up_button = Button(self.__screen_saver_frame, image = self.__saver_img , command = self.go_to_login_screen)
        wake_up_button.grid(row=0,column=0,sticky='NSEW')


    def go_to_login_screen(self):
        LogIn_screen.getInstance().rise_frame()
        Screen_manager.get_root().after(constants.SCREEN_SAVER_BACK_TIMER, lambda:self.__screen_saver_frame.tkraise())
