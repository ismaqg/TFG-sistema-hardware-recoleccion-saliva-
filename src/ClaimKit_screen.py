from time import time
from tkinter import *
from tkinter import messagebox
from Not_available import Not_available
from Person import ActivePerson

import Screen_manager
import constants
import Checker
import Arduino_controller
import Counters
import DBcontroller
from SubmitSample_screen import SubmitSample_screen

class ClaimKit_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if ClaimKit_screen.__instance == None:
            ClaimKit_screen()
        return ClaimKit_screen.__instance

    def __init__(self):
        if ClaimKit_screen.__instance != None:
            raise Exception("ClaimKit_screen class is singleton")
        else:

            self.__claimKitscreen_frame = Screen_manager.init_screen_frame()
            self.__claimKitscreen_header_frame = Screen_manager.header_frame(self.__claimKitscreen_frame)
            self.__claimKitscreen_body_frame = Screen_manager.body_frame(self.__claimKitscreen_frame)

            self.__title = Label(self.__claimKitscreen_header_frame, text = "OBTENER KIT", bg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_TITLE_TEXT_SIZE, 'bold'))
            self.__return_b = Button(self.__claimKitscreen_header_frame, text = "VOLVER\nATRÁS", borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__return_b.grid(row = 0, column = 1, sticky = 'NSEW', pady=10, padx=10)

            self.__claimKitscreen_header_frame.columnconfigure(0, weight=5)
            self.__claimKitscreen_header_frame.columnconfigure(1, weight=1)
            self.__claimKitscreen_header_frame.rowconfigure(0, weight=1)  # it's necessary to give a weight (even though there is only one row in clamKitscreen_header_frame) for sticky=NSEW of the inside widgets to work correctly


            self.__previous_info_title = Label(self.__claimKitscreen_body_frame, text = "INFORMACIÓN PREVIA:", bg = "white", fg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
            self.__previous_info_displayer = Text(self.__claimKitscreen_body_frame, font = (constants.CATSALUT_TEXT_FONT, constants.PARAGRAPH_TEXT_SIZE), height = 6, wrap = WORD)  # height hardcoded to 6 because we want 6 lines of "previous information" to be showed on this screen on the raspberry 
            self.__previous_info_displayer.insert(INSERT, constants.PREVIOUS_INFO_SALIVA_TEST)
            self.__previous_info_displayer["state"] = DISABLED  # No changes can be done to the previous info text box at this point
            self.__get_kit_b = Button(self.__claimKitscreen_body_frame, text = "Cumplo los requisitos.\n Quiero recoger el kit", borderwidth=3, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__get_kit)

            self.__previous_info_title.grid(row = 0, column = 0, sticky = 'NSEW', pady=5)
            self.__previous_info_displayer.grid(row = 1, column = 0, sticky = 'NSEW', padx = 20)
            self.__get_kit_b.grid(row = 2, column=0, sticky = 'NSEW', padx=150, pady=5)

            self.__claimKitscreen_body_frame.rowconfigure(0, weight = 1)
            self.__claimKitscreen_body_frame.rowconfigure(1, weight = 3)
            self.__claimKitscreen_body_frame.rowconfigure(2, weight = 1)
            self.__claimKitscreen_body_frame.columnconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one column in clamKitscreen_body_frame) for sticky=NSEW of the inside widgets to work correctly
            

            ClaimKit_screen.__instance = self

    


    def __previous_screen(self):
        from MainScreen_user import MainScreen_user  # declared here to avoid circular dependency. It cannot be declared at the beggining of the file cannot be declared at the top of the file or in the constructor
        MainScreen_user.getInstance().go_to_main_screen()


    def __get_kit(self):
        if (Checker.is_arduino_alive()):

            # TODO: Pedirle el kit al arduino y programar un timeout que puede saltar si tarda mucho
            
            timeout = False  # TODO: cambiarlo por lo del TODO anterior. La variablerepresenta timeout en la accion de abrir la puerta y dejar caer kit

            if timeout:
                Arduino_controller.inoperative_arduino_actions()
            else:  # arduino ha abierto correctamente la puerta y ha dejado caer un kit 
                Counters.decrement_available_kits()
                DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "COLLECTED KIT")  # to info_uso DB
                if DBcontroller.user_has_kit():
                    DBcontroller.update_time_pickup_kit()  # to muestras_saliva DB
                else:
                    DBcontroller.add_new_record_with_pickup_kit()  # to muestras_saliva DB
                messagebox.showinfo("RECOGIDA KIT", "Ya puedes recoger el kit del depósito lateral. Será redirigido al menú de entrega de muestra de saliva, donde se le mostrarán las instrucciones") # TODO: No sé si es un depósito lateral, igual tengo que cambiar esto
                ActivePerson.getCurrent().set_has_claimed_kit_to_true()

                # TODO: No sé si hace falta decirle explícitamente al arduino que cierre la compuerta. En ese caso, añadirlo aquí (con su respectivo timeout por si se quedase pillado al cerrarla)

                SubmitSample_screen.getInstance().go_to_submitSample_screen()
                
        else:
            Arduino_controller.inoperative_arduino_actions()

    


    def go_to_claimKit_screen(self):
        self.__claimKitscreen_frame.tkraise()