from tkinter import *

import constants


class Numerical_keyboard:

    def __init__(self, keyboard_title, default_value):

        # info about the number introduced
        self.__is_keyboard_alive = TRUE
        self.__is_number_introduced = FALSE
        self.__number_introduced = default_value

        # new toplevel window
        self.__keyboard_window = Toplevel()
        width = int(constants.SCREEN_WIDTH/2)
        height = constants.SCREEN_HEIGHT
        xoffset = int(constants.SCREEN_WIDTH/4) # the widget will start in 1/4 of the screen and thus occupy the middle of the screen
        yoffset = 0
        self.__keyboard_window.geometry( str(width) + "x" + str(height) + "+" + str(xoffset) + "+" + str(yoffset))

        #ELIMINATE THE UPPER BAR AND MAKES THAT THE WINDOW CANNOT DISAPPEAR FROM THE SCREEN, NOT EVEN BY CLICKING ON THE ROOT WINDOW:
        self.__keyboard_window.overrideredirect(True)

        # label and entry of the new window
        title = Label(self.__keyboard_window, text = keyboard_title, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
        title.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
        self.__entry = Entry(self.__keyboard_window, borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
        self.__entry.insert(0, str(default_value))
        self.__entry.grid(row = 1, column = 0, columnspan = 3, sticky = 'NSEW')

        # buttons of the new window
        Button(self.__keyboard_window, text="1", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(1)).grid(row = 2, column = 0, sticky = 'NSEW')
        Button(self.__keyboard_window, text="2", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(2)).grid(row = 2, column = 1, sticky = 'NSEW')
        Button(self.__keyboard_window, text="3", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(3)).grid(row = 2, column = 2, sticky = 'NSEW')
        Button(self.__keyboard_window, text="4", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(4)).grid(row = 3, column = 0, sticky = 'NSEW')
        Button(self.__keyboard_window, text="5", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(5)).grid(row = 3, column = 1, sticky = 'NSEW')
        Button(self.__keyboard_window, text="6", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(6)).grid(row = 3, column = 2, sticky = 'NSEW')
        Button(self.__keyboard_window, text="7", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(7)).grid(row = 4, column = 0, sticky = 'NSEW')
        Button(self.__keyboard_window, text="8", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(8)).grid(row = 4, column = 1, sticky = 'NSEW')
        Button(self.__keyboard_window, text="9", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(9)).grid(row = 4, column = 2, sticky = 'NSEW')
        Button(self.__keyboard_window, text="   0   ", font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE), command=lambda: self.__button_click(0)).grid(row = 5, column = 1, sticky = 'NSEW')  # note that the character to display is not "0" but "0     ". This is to make this column as wide as the other columns
        Button(self.__keyboard_window, text=" CLEAR ", fg = "red", font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = self.__clear).grid(row = 5, column = 0, sticky = 'NSEW')
        Button(self.__keyboard_window, text="ACCEPT", fg = "green", font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = self.__accept).grid(row = 5, column = 2, sticky = 'NSEW')
        Button(self.__keyboard_window, text="EXIT", fg = "red", borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = self.__exit).grid(row = 0, column = 2, sticky = 'NSEW', padx=25, pady=25)

        # rows and columns config
        self.__keyboard_window.rowconfigure(0, weight = 1)
        self.__keyboard_window.rowconfigure(1, weight = 1)
        self.__keyboard_window.rowconfigure(2, weight = 1)
        self.__keyboard_window.rowconfigure(3, weight = 1)
        self.__keyboard_window.rowconfigure(4, weight = 1)
        self.__keyboard_window.rowconfigure(5, weight = 1)
        self.__keyboard_window.columnconfigure(0, weight = 1)
        self.__keyboard_window.columnconfigure(1, weight = 1)
        self.__keyboard_window.columnconfigure(2, weight = 1)



    def is_number_introduced(self):
        return self.__is_number_introduced

    def get_number_introduced(self):
        return self.__number_introduced

    def is_keyboard_alive(self):
        return self.__is_keyboard_alive


    def __button_click(self, number):
        self.__entry.insert(END, str(number))

    def __clear(self):
        self.__entry.delete(0, END)

    def __accept(self):
        self.__is_number_introduced = TRUE
        self.__number_introduced = int(self.__entry.get())
        self.__keyboard_window.destroy()

    def __exit(self):
        self.__is_keyboard_alive = FALSE
        self.__keyboard_window.destroy()
