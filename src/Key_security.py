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
        root_width = constants.SCREEN_WIDTH
        root_height = constants.SCREEN_HEIGHT
        self.__key_window.geometry( str(int(root_width/2)) + "x" + str(root_height) )

        #ELIMINATE THE UPPER BAR AND MAKES THAT THE WINDOW CANNOT DISAPPEAR FROM THE SCREEN, NOT EVEN BY CLICKING ON THE ROOT WINDOW:
        self.__key_window.overrideredirect(True)


        # label and entry of the new window
        title = Label(self.__key_window, text = "Introduce your access key")
        title.grid(row = 0, column = 0, columnspan = 3, sticky = 'NSEW')
        self.__entry = Entry(self.__key_window, borderwidth=5)
        self.__entry.grid(row = 1, column = 0, columnspan = 3, sticky = 'NSEW')

        # buttons of the new window
        Button(self.__key_window, text="1", command=lambda: self.__button_click(1)).grid(row = 2, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="2", command=lambda: self.__button_click(2)).grid(row = 2, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="3", command=lambda: self.__button_click(3)).grid(row = 2, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="4", command=lambda: self.__button_click(4)).grid(row = 3, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="5", command=lambda: self.__button_click(5)).grid(row = 3, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="6", command=lambda: self.__button_click(6)).grid(row = 3, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="7", command=lambda: self.__button_click(7)).grid(row = 4, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="8", command=lambda: self.__button_click(8)).grid(row = 4, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="9", command=lambda: self.__button_click(9)).grid(row = 4, column = 2, sticky = 'NSEW')
        Button(self.__key_window, text="0", command=lambda: self.__button_click(0)).grid(row = 5, column = 1, sticky = 'NSEW')
        Button(self.__key_window, text="CLEAR", fg = "red", command = self.__clear).grid(row = 5, column = 0, sticky = 'NSEW')
        Button(self.__key_window, text="ACCEPT", fg = "green", command = self.__accept).grid(row = 5, column = 2, sticky = 'NSEW')

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
        key_introduced = self.__entry.get()
        if len(key_introduced) != len(constants.CORRECT_PASSWORD):
            self.__entry.delete(0, END)
            messagebox.showerror("LONGITUD DE CLAVE INCORRECTA", "La clave debe ser de " + str(constants.CORRECT_PASSWORD) + " números")
        else:
            self.__key_introduced = TRUE
            if (key_introduced == constants.CORRECT_PASSWORD):
                self.__key_is_correct = TRUE
            self.__key_window.destroy()

    @staticmethod
    def __ignore_event():
        pass