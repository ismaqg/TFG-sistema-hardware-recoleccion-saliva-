from tkinter import *
from tkinter import messagebox

import Screen_manager
import constants
from Key_security import Key_security

# en esta screen simplemente se pondria una label de "maquina inoperativa" que y haya un boton de "cerrar programa" donde se pedirá la contraseña de los admins y, si se pone bien, saldra un mensaje diciendo que se arreglen los errores y se vuelva a reiniciar el programa y entonces se cerrará el programa.


class Not_available: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if Not_available.__instance == None:
            Not_available()
        return Not_available.__instance

    def __init__(self):
        if Not_available.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("Not_available class is singleton")
        else:

            self.__not_available_screen_frame = Screen_manager.init_screen_frame()

            self.__not_available_label = Label(self.__not_available_screen_frame, text = "NO DISPONIBLE", font= (constants.CATSALUT_TEXT_FONT, constants.APP_NOT_AVAILABLE_ERROR_TEXT_SIZE, 'bold') , bg = "white", fg = "red")
            self.__not_available_label.grid(row=1, column=0, columnspan=3, sticky='NSEW')

            self.__quit_b = Button(self.__not_available_screen_frame, text = "CERRAR PROGRAMA", bg = constants.LIGHT_RED_BACKGROUNDCOLOR, fg = "red", borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__quit_program_wrapper)
            self.__quit_b.grid(row=2, column=1, sticky='NSEW')

            self.__not_available_screen_frame.rowconfigure(0, weight=1)
            self.__not_available_screen_frame.rowconfigure(1, weight=3)
            self.__not_available_screen_frame.rowconfigure(2, weight=1)
            self.__not_available_screen_frame.columnconfigure(0, weight=1)
            self.__not_available_screen_frame.columnconfigure(1, weight=1)
            self.__not_available_screen_frame.columnconfigure(2, weight=1)


            Not_available.__instance = self

    # this wrapper is needed because key_security can only be instantiated 1 time to work correctly, and the other function is recalled every 500ms until a password is typed in
    def __quit_program_wrapper(self):
        admin_or_operator_check = Key_security() 
        self.__quit_program(admin_or_operator_check)

    def __quit_program(self, admin_or_operator_check):
        if not admin_or_operator_check.key_introduced():
            # program to check the key input after another 0.5 seconds:
            Screen_manager.get_root().after(500, lambda:self.__quit_program(admin_or_operator_check))
        elif admin_or_operator_check.password_is_correct():
            Screen_manager.get_root().destroy()
            # no "new event", because the event APP CLOSED. ARDUINO INOPERATIVE has already been registered on the get kit screen
        else:
            messagebox.showwarning("ACCESO DENEGADO", "Clave errónea")

    def go_to_not_available_screen(self):
        self.__not_available_screen_frame.tkraise()