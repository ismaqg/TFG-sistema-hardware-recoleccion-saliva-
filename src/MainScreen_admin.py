from tkinter import *

from MainScreen import MainScreen
from Query_DB_screen import Query_DB_screen
import Counters
import constants


class MainScreen_admin(MainScreen):  # singleton 

    __instance = None

    @staticmethod
    def getInstance():
        if MainScreen_admin.__instance == None:
            MainScreen_admin()
        return MainScreen_admin.__instance

    def __init__(self):
        if MainScreen_admin.__instance != None:
            raise Exception("MainScreen_admin class is singleton")
        else:
            MainScreen.create_main_frames()

            # NO .grid, because the main_screen_frame is shared with other classes. The .grid is done in "go_to_main_screen"

            self.__title = Label(MainScreen._ms_header_frame, text = "ADMINISTRADOR", bg = constants.CATSALUT_COLOR, font = ("Verdana", 26, 'bold'))
            self.__logout_b = Button(MainScreen._ms_header_frame, text = "CERRAR\nSESIÓN", bg = constants.LIGHT_GRAY_BACKGROUNDCOLOR, borderwidth=3, font = ("Verdana", 22, 'bold'), command = self.logOut) 
            self.__quit_program_b = Button(MainScreen._ms_header_frame, text = "APAGAR", bg = constants.LIGHT_RED_BACKGROUNDCOLOR, fg = "red", borderwidth=3, font = ("Verdana", 22, 'bold'), command = self.__quit_program)

            MainScreen._ms_header_frame.columnconfigure(0, weight = 4)
            MainScreen._ms_header_frame.columnconfigure(1, weight = 1)
            MainScreen._ms_header_frame.columnconfigure(2, weight = 1)
            MainScreen._ms_header_frame.rowconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one row in ms_header_frame) for sticky=NSEW of title, logout_b and quit_program_b to work correctly


            self.__remaining_labels_info = Label(MainScreen._ms_body_frame, text = "Etiquetas impresora restantes: " + str(Counters.get_available_labels()) + " de " + str(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL), font = ("Verdana", 12, 'bold'), borderwidth=2, relief="groove", fg = Counters.get_available_labels_fg_color(), bg = Counters.get_available_labels_bg_color())
            self.__remaining_kits_info = Label(MainScreen._ms_body_frame, text = "Kits restantes: " + str(Counters.get_available_kits()) + " de " + str(constants.AVAILABLE_KITS_AFTER_REFILL), font = ("Verdana", 12, 'bold'), borderwidth=2, relief="groove", fg = Counters.get_available_kits_fg_color(), bg = Counters.get_available_kits_bg_color())
            self.__stored_samples_info = Label(MainScreen._ms_body_frame, text = "Muestras entregadas: " + str(Counters.get_stored_samples()) + " (max: " + str(constants.STORED_SAMPLES_LIMIT) +")", font = ("Verdana", 12, 'bold'), borderwidth=2, relief="groove", fg = Counters.get_stored_samples_fg_color(), bg = Counters.get_stored_samples_bg_color())

            self.__refill_kits_b = Button(MainScreen._ms_body_frame, text = "REPONER\nKITS", font = ("Verdana", 22, 'bold'), command = self.__refill_kits)
            self.__refill_labels_b = Button(MainScreen._ms_body_frame, text = "REPONER\nETIQUETAS\nIMPRESORA", font = ("Verdana", 22, 'bold'), command = self.__refill_labels)
            self.__collect_samples_b = Button(MainScreen._ms_body_frame, text = "RECOGER\nMUESTRAS", font = ("Verdana", 22, 'bold'), command = self.__collect_samples)
            self.__check_DB_b = Button(MainScreen._ms_body_frame, text = "CONSULTAR\nBASE DE DATOS", font = ("Verdana", 22, 'bold'), command = Query_DB_screen.getInstance().go_to_query_DB_screen) # no need to grid_forget() when switching to the DB_screen, because if you then go back from there to main_screen, the buttons you should see are the same

            MainScreen._ms_body_frame.rowconfigure(0, weight = 1)
            MainScreen._ms_body_frame.rowconfigure(1, weight = 4)
            MainScreen._ms_body_frame.rowconfigure(2, weight = 4)
            MainScreen._ms_body_frame.columnconfigure(0, weight = 1)
            MainScreen._ms_body_frame.columnconfigure(1, weight = 1)
            MainScreen._ms_body_frame.columnconfigure(2, weight = 1)
            MainScreen._ms_body_frame.columnconfigure(3, weight = 1)
            MainScreen._ms_body_frame.columnconfigure(4, weight = 1)
            MainScreen._ms_body_frame.columnconfigure(5, weight = 1)

            MainScreen_admin.__instance = self

    @staticmethod
    def __quit_program():
        # TODO: guardar evento programa apagado en BD y matar la aplicacion. Y, hacer un shutdown now de la rpi por codigo (y en el bashrc de la rpi hacer que se lance esta aplicacion directamente)
        pass

    @staticmethod
    def __refill_kits():
        # TODO now: Llamar a Counters.set_kits(constants.KITSAFTERREFILL) + un showmessage por pantalla indicando el exito + actualizar label que indica cuantos kits quedan (y el color). Y suponemos que por hardware no hay que hacer nada (abren el lateral con llave)
        # TODO futuro: Que el que hace refill tenga la posibilidad de indicar cuantos AÑADE, por si no llena el deposito entero. En ese caso, el valor de kits será el que había más el añadido
        pass

    @staticmethod
    def __refill_labels():
        # TODO now: Llamar a Counters.set_labels(constants.LABELSAFTERREFILL) + un showmessage por pantalla indicando el exito + actualizar label que indica cuantas etiquetas de impresora quedan (y el color)
        pass

    @staticmethod
    def __collect_samples():
        # TODO now: Llamar a Counters.set_samples(0) + un showmessage por pantalla indicando el exito + actualizar label que indica cuantos samples hay (y el color). Y suponemos que por hardware no hay que hacer nada (abren el lateral con llave)
        pass


    # override parent method
    def go_to_main_screen(self):
        self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
        self.__logout_b.grid(row = 0, column = 1, sticky = 'NSEW', padx = (10, 5), pady = 10)
        self.__quit_program_b.grid(row = 0, column = 2, sticky = 'NSEW', padx = (5, 10), pady = 10)

        self.__remaining_labels_info.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
        self.__remaining_kits_info.grid(row = 0, column = 2, columnspan = 2, sticky = 'NSEW')
        self.__stored_samples_info.grid(row = 0, column = 4, columnspan = 2, sticky = 'NSEW')

        self.__refill_kits_b.grid(row = 1, column = 0, columnspan = 3, sticky = 'NSEW', padx = (10, 5), pady = (10, 5))
        self.__refill_labels_b.grid(row = 1, column = 3, columnspan = 3, sticky = 'NSEW', padx = (5, 10), pady = (10, 5))
        self.__collect_samples_b.grid(row = 2, column = 0, columnspan = 3, sticky = 'NSEW', padx = (10, 5), pady = (5, 10))
        self.__check_DB_b.grid(row = 2, column = 3, columnspan = 3, sticky = 'NSEW', padx = (5, 10), pady = (5, 10))

        MainScreen._main_screen_frame.tkraise()

    # override parent method
    def _erase_mainScreen_contents(self):
        self.__title.grid_forget()
        self.__logout_b.grid_forget()
        self.__quit_program_b.grid_forget()

        self.__remaining_labels_info.grid_forget()
        self.__remaining_kits_info.grid_forget()
        self.__stored_samples_info.grid_forget()

        self.__refill_kits_b.grid_forget()
        self.__refill_labels_b.grid_forget()
        self.__collect_samples_b.grid_forget()
        self.__check_DB_b.grid_forget()

    def logOut(self):
        self._erase_mainScreen_contents()
        super().logOut()
        pass