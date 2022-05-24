from tkinter import *

import hashlib

import constants
import Language_controller



class Key_security:

    def __init__(self):

        # info about the password:
        self.__key_introduced = FALSE
        self.__key_is_correct = FALSE

        # new toplevel window
        self.__key_window = Toplevel()
        width = int(constants.SCREEN_WIDTH/2)
        height = constants.SCREEN_HEIGHT
        xoffset = int(constants.SCREEN_WIDTH/4) # the widget will start in 1/4 of the screen and thus occupy the middle of the screen
        yoffset = 0
        self.__key_window.geometry( str(width) + "x" + str(height) + "+" + str(xoffset) + "+" + str(yoffset))

        #ELIMINATE THE UPPER BAR AND MAKES THAT THE WINDOW CANNOT DISAPPEAR FROM THE SCREEN, NOT EVEN BY CLICKING ON THE ROOT WINDOW:
        self.__key_window.overrideredirect(True)


        # label and entry of the new window
        title = Label(self.__key_window, text = Language_controller.get_message("introduce tu clave de acceso"), font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
        title.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
        self.__entry = Entry(self.__key_window, borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
        self.__entry.grid(row = 1, column = 0, columnspan = 3, sticky = 'NSEW')

        # buttons of the new window
        Button(self.__key_window, text="1", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(1)).grid(row = 2, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="2", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(2)).grid(row = 2, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="3", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(3)).grid(row = 2, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="4", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(4)).grid(row = 3, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="5", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(5)).grid(row = 3, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="6", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(6)).grid(row = 3, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="7", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(7)).grid(row = 4, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="8", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(8)).grid(row = 4, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="9", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(9)).grid(row = 4, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="   0   ", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(0)).grid(row = 5, column = 1, sticky = 'NSEW')  # note that the character to display is not "0" but "0     ". This is to make this column as wide as the other columns
        Button(self.__key_window, text=" CLEAR ", fg = "red", font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = self.__clear).grid(row = 5, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="ACCEPT", fg = "green", font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = self.__accept).grid(row = 5, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="EXIT", fg = "red", borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = self.__exit).grid(row = 0, column = 2, sticky = 'NSEW', padx=25, pady=25)

        # rows and columns config
        self.__key_window.rowconfigure(0, weight = 1)
        self.__key_window.rowconfigure(1, weight = 1)
        self.__key_window.rowconfigure(2, weight = 1)
        self.__key_window.rowconfigure(3, weight = 1)
        self.__key_window.rowconfigure(4, weight = 1)
        self.__key_window.rowconfigure(5, weight = 1)
        self.__key_window.columnconfigure(0, weight = 1)
        self.__key_window.columnconfigure(1, weight = 1)
        self.__key_window.columnconfigure(2, weight = 1)



    def key_introduced(self):
        return self.__key_introduced

    def password_is_correct(self):
        return self.__key_is_correct


    def __button_click(self, number):
        self.__entry.insert(END, str(number))

    def __clear(self):
        self.__entry.delete(0, END)

    def __accept(self):
        self.__key_introduced = TRUE
        if (hashlib.sha256( str.encode(self.__entry.get()) ).hexdigest() == constants.CORRECT_PASSWORD_ENCRIPTED):
            self.__key_is_correct = TRUE
        self.__key_window.destroy()

    def __exit(self):
        self.__key_introduced = TRUE
        self.__key_is_correct = FALSE
        self.__key_window.destroy()
