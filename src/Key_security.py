from tkinter import *
from tkinter import messagebox
import constants
import Screen_manager



class Key_security:

    def __init__(self):

        # info about the password:
        self.__key_introduced = FALSE
        self.__key_is_correct = FALSE

        # new toplevel window
        self.__key_window = Toplevel()
        self.__key_window.title("Introduce your access key")
        width = int(constants.SCREEN_WIDTH/2)
        height = constants.SCREEN_HEIGHT
        xoffset = int(constants.SCREEN_WIDTH/2) # the widget will start in the middle of the screen and thus occupy the right half of the screen
        yoffset = 0
        self.__key_window.geometry( str(width) + "x" + str(height) + "+" + str(xoffset) + "+" + str(yoffset))

        #ELIMINATE THE UPPER BAR AND MAKES THAT THE WINDOW CANNOT DISAPPEAR FROM THE SCREEN, NOT EVEN BY CLICKING ON THE ROOT WINDOW:
        self.__key_window.overrideredirect(True)


        # label and entry of the new window
        title = Label(self.__key_window, text = "Introduce tu clave de acceso", font = ("Verdana", 22, 'bold'))
        title.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
        self.__entry = Entry(self.__key_window, borderwidth=5, font = ("Verdana", 26, 'bold'))
        self.__entry.grid(row = 1, column = 0, columnspan = 3, sticky = 'NSEW')

        # buttons of the new window
        Button(self.__key_window, text="1", font = ("Verdana", 22), command=lambda: self.__button_click(1)).grid(row = 2, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="2", font = ("Verdana", 22), command=lambda: self.__button_click(2)).grid(row = 2, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="3", font = ("Verdana", 22), command=lambda: self.__button_click(3)).grid(row = 2, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="4", font = ("Verdana", 22), command=lambda: self.__button_click(4)).grid(row = 3, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="5", font = ("Verdana", 22), command=lambda: self.__button_click(5)).grid(row = 3, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="6", font = ("Verdana", 22), command=lambda: self.__button_click(6)).grid(row = 3, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="7", font = ("Verdana", 22), command=lambda: self.__button_click(7)).grid(row = 4, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="8", font = ("Verdana", 22), command=lambda: self.__button_click(8)).grid(row = 4, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="9", font = ("Verdana", 22), command=lambda: self.__button_click(9)).grid(row = 4, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="0", font = ("Verdana", 22), command=lambda: self.__button_click(0)).grid(row = 5, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="CLEAR", fg = "red", font = ("Verdana", 22, 'bold'), command = self.__clear).grid(row = 5, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="ACCEPT", fg = "green", font = ("Verdana", 22, 'bold'), command = self.__accept).grid(row = 5, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="EXIT", fg = "red", bg = "#c0c0c0", borderwidth=3, font = ("Verdana", 22, 'bold'), command = self.__exit).grid(row = 0, column = 2, sticky = 'NSEW', padx=25, pady=25)

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
        if (self.__entry.get() == constants.CORRECT_PASSWORD):
            self.__key_is_correct = TRUE
        self.__key_window.destroy()

    def __exit(self):
        self.__key_introduced = TRUE
        self.__key_is_correct = FALSE
        self.__key_window.destroy()
