from time import time
from tkinter import *
from tkinter import messagebox
from Not_available_screen import Not_available_screen
from Person import ActivePerson

import Screen_manager
import constants
import Checker
import Arduino_controller
import Counters
import DBcontroller
import Language_controller
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
            Screen_manager.get_root().destroy()
            raise Exception("ClaimKit_screen class is singleton")
        else:

            self.__claimKitscreen_frame = Screen_manager.init_screen_frame()
            self.__claimKitscreen_header_frame = Screen_manager.header_frame(self.__claimKitscreen_frame)
            self.__claimKitscreen_body_frame = Screen_manager.body_frame(self.__claimKitscreen_frame)

            self.__title = Label(self.__claimKitscreen_header_frame, text = Language_controller.get_message("título obtener kit"), bg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_TITLE_TEXT_SIZE, 'bold'))
            self.__return_b = Button(self.__claimKitscreen_header_frame, text = Language_controller.get_message("volver atrás"), borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__return_b.grid(row = 0, column = 1, sticky = 'NSEW', pady=10, padx=10)

            self.__claimKitscreen_header_frame.columnconfigure(0, weight=5)
            self.__claimKitscreen_header_frame.columnconfigure(1, weight=1)
            self.__claimKitscreen_header_frame.rowconfigure(0, weight=1)  # it's necessary to give a weight (even though there is only one row in clamKitscreen_header_frame) for sticky=NSEW of the inside widgets to work correctly


            self.__previous_info_title = Label(self.__claimKitscreen_body_frame, text = Language_controller.get_message("información previa (cabecera)"), bg = "white", fg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
            self.__previous_info_displayer = Text(self.__claimKitscreen_body_frame, font = (constants.CATSALUT_TEXT_FONT, constants.PARAGRAPH_TEXT_SIZE), height = 6, wrap = WORD)  # height hardcoded to 6 because we want 6 lines of "previous information" to be showed on this screen on the raspberry 
            self.__previous_info_displayer.insert(INSERT, Language_controller.get_message("información previa (extendida)"))
            self.__previous_info_displayer["state"] = DISABLED  # No changes can be done to the previous info text box at this point
            self.__get_kit_b = Button(self.__claimKitscreen_body_frame, text = Language_controller.get_message("quiero recoger un kit"), borderwidth=3, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__get_kit)
            self.__dont_get_kit_b = Button(self.__claimKitscreen_body_frame, text = Language_controller.get_message("no cumplo los requisitos"), borderwidth=3, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), bg = constants.LIGHT_RED_BACKGROUNDCOLOR, command = self.__dont_meet_requirements)

            self.__previous_info_title.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW', pady=5)
            self.__previous_info_displayer.grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW', padx = 20)
            self.__get_kit_b.grid(row = 2, column=0, sticky = 'NSEW', padx=(20,10), pady=5)
            self.__dont_get_kit_b.grid(row = 2, column=1, sticky = 'NSEW', padx=(10,20), pady=5)

            self.__claimKitscreen_body_frame.rowconfigure(0, weight = 1)
            self.__claimKitscreen_body_frame.rowconfigure(1, weight = 3)
            self.__claimKitscreen_body_frame.rowconfigure(2, weight = 1)
            self.__claimKitscreen_body_frame.columnconfigure(0, weight = 1)
            self.__claimKitscreen_body_frame.columnconfigure(1, weight = 1) 
            

            ClaimKit_screen.__instance = self

    


    def __previous_screen(self):
        from MainScreen_user import MainScreen_user  # declared here to avoid circular dependency. It cannot be declared at the beggining of the file cannot be declared at the top of the file or in the constructor
        MainScreen_user.getInstance().go_to_main_screen()


    def __get_kit(self):
        # TODO: Pedirle el kit al arduino (hacer girar el motor y que pare cuando detectemos que ha caido el kit). Todo lo de arduino con timeouts y tal obviamente
                   
        Counters.decrement_available_kits()
        DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "COLLECTED KIT")  # to info_uso DB
        if DBcontroller.user_has_kit():
            DBcontroller.update_time_pickup_kit()  # to muestras_saliva DB
        else:
            DBcontroller.add_new_record_with_pickup_kit()  # to muestras_saliva DB
        messagebox.showinfo(Language_controller.get_message("kit dispensado (cabecera)"), Language_controller.get_message("kit dispensado (cuerpo)")) # TODO: No sé si es un depósito lateral, igual tengo que cambiar el mensaje
        ActivePerson.getCurrent().set_has_claimed_kit_to_true()
        SubmitSample_screen.getInstance().go_to_submitSample_screen()



    def __dont_meet_requirements(self):
        ActivePerson.getCurrent().logOut()  # This function can't be called directly on the "command" parameter of the dont_get_kit_b button instantiation because, if we do that, as soon as the ClaimKit_screen object is created, ActivePerson.getCurrent()
                                            # would be called in order to prepare the instance/class which contains that "logout()" function that we want to "link" with the dont_get_kit_b button. And at that momment there is no "Current" inside "Person", so an exception would be thrown!



    
    # changes the texts to the current language. This function is called by Language_controller when a new language is setted
    def change_language(self):
        self.__title["text"] = Language_controller.get_message("título obtener kit")
        self.__return_b["text"] = Language_controller.get_message("volver atrás")
        self.__previous_info_title["text"] = Language_controller.get_message("información previa (cabecera)")
        self.__previous_info_displayer["state"] = NORMAL
        self.__previous_info_displayer.delete('1.0', END)
        self.__previous_info_displayer.insert(INSERT, Language_controller.get_message("información previa (extendida)"))
        self.__previous_info_displayer["state"] = DISABLED
        self.__get_kit_b["text"] = Language_controller.get_message("quiero recoger un kit")
        self.__dont_get_kit_b["text"] = Language_controller.get_message("no cumplo los requisitos")

    def go_to_claimKit_screen(self):
        self.__claimKitscreen_frame.tkraise()