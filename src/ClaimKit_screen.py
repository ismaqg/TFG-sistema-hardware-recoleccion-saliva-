from tkinter import *

import Screen_manager
import constants
import Checker

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
            self.__previous_info_displayer = Text(self.__claimKitscreen_body_frame, font = (constants.CATSALUT_TEXT_FONT, constants.PARAGRAPH_TEXT_SIZE), wrap = WORD)
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

    @staticmethod
    def __get_kit():
        # TODO: Ver si arduino está vivo; si no está pues enviar mensaje y poner problema por pantalla y que se le cerrará sesión y que vuelva mas tarde y tal.
        # TODO: En caso de arduino vivo: pedirle el kit (aun así con un timeout). Si salta el timeout hacer lo del if anterior, y si no salta pues llamar a decrementar variable kits disponibles + Registrar en las 2 BD (en la de muestras_saliva: si ya habia peido kits antes sin entregar pues actualizamos la hora de la ultima vez que ha pedido kit y si no creamos nueva entrada) + avisarle que ya puede recoger el kit en el lado + ActivePerson.getCurrent.set_has_claimed_kit_to_true() + llevarlo al menú de ENTREGAR MUESTRA SALIVA después de unos segundos.
        pass

    def go_to_claimKit_screen(self):
        self.__claimKitscreen_frame.tkraise()