from tkinter import *
import Screen_manager

class LogIn_screen(): #singleton

    __instance = None

    @staticmethod 
    def getInstance():
        if LogIn_screen.__instance == None:
            LogIn_screen()
        return LogIn_screen.__instance

    def __init__(self):
        if LogIn_screen.__instance != None:
            raise Exception("LogIn_screen class is singleton")
        else:
            self.__login_screen_frame = Screen_manager.init_screen_frame()
            self.__login_header_frame = Screen_manager.header_frame(self.__login_screen_frame)
            self.__login_body_frame = Screen_manager.header_frame(self.__login_screen_frame)
            LogIn_screen.__instance = self


    def rise_frame(self):
        self.__login_screen_frame.tkraise()

