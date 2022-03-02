from tkinter import *
from tkinter import messagebox

from MainScreen import MainScreen
from Query_DB_screen import Query_DB_screen
from Person import ActivePerson
import Counters
import constants
import DBcontroller
import Screen_manager
import Language_controller

class MainScreen_operator(MainScreen):  # singleton 

    __instance = None

    @staticmethod
    def getInstance():
        if MainScreen_operator.__instance == None:
            MainScreen_operator()
        return MainScreen_operator.__instance

    def __init__(self):
        if MainScreen_operator.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("MainScreen_operator class is singleton")
        else:
            MainScreen.create_main_frames()

            # NO .grid, because the main_screen_frame is shared with other classes. The .grid is done in "go_to_main_screen"

            self.__title = Label(MainScreen._ms_header_frame, text = Language_controller.get_message("título operario"), bg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_TITLE_TEXT_SIZE, 'bold'))
            self.__logout_b = Button(MainScreen._ms_header_frame, text = Language_controller.get_message("texto botón cerrar sesión para admin/operador"), borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.logOut_button) 
            self.__quit_program_b = Button(MainScreen._ms_header_frame, text = Language_controller.get_message("apagar"), bg = constants.LIGHT_RED_BACKGROUNDCOLOR, fg = "red", borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = super()._quit_program)

            self.__remaining_labels_info = Label(MainScreen._ms_body_frame, text = Language_controller.get_message("avisador etiquetas restantes") + str(Counters.get_available_labels()) + Language_controller.get_message("de") + str(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL), font = (constants.CATSALUT_TEXT_FONT, constants.CONTROL_INFORMATION_TEXT_SIZE, 'bold'), borderwidth=2, relief="groove", fg = Counters.get_available_labels_fg_color(), bg = Counters.get_available_labels_bg_color())
            self.__remaining_kits_info = Label(MainScreen._ms_body_frame, text = Language_controller.get_message("avisador kits restantes") + str(Counters.get_available_kits()) + Language_controller.get_message("de") + str(constants.AVAILABLE_KITS_AFTER_REFILL), font = (constants.CATSALUT_TEXT_FONT, constants.CONTROL_INFORMATION_TEXT_SIZE, 'bold'), borderwidth=2, relief="groove", fg = Counters.get_available_kits_fg_color(), bg = Counters.get_available_kits_bg_color())
            self.__stored_samples_info = Label(MainScreen._ms_body_frame, text = Language_controller.get_message("avisador muestras entregadas") + str(Counters.get_stored_samples()) + " (max: " + str(constants.STORED_SAMPLES_LIMIT) + ")", font = (constants.CATSALUT_TEXT_FONT, constants.CONTROL_INFORMATION_TEXT_SIZE, 'bold'), borderwidth=2, relief="groove", fg = Counters.get_stored_samples_fg_color(), bg = Counters.get_stored_samples_bg_color())

            self.__refill_kits_b = Button(MainScreen._ms_body_frame, text = Language_controller.get_message("reponer kits"), font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), borderwidth=5, command = self.__refill_kits)
            self.__refill_labels_b = Button(MainScreen._ms_body_frame, text = Language_controller.get_message("reponer etiquetas"), font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), borderwidth=5, command = self.__refill_labels)
            self.__collect_samples_b = Button(MainScreen._ms_body_frame, text = Language_controller.get_message("recoger muestras"), font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), borderwidth=5, command = self.__collect_samples)
            self.__check_DB_b = Button(MainScreen._ms_body_frame, text = Language_controller.get_message("consultar BD"), font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), borderwidth=5, command = Query_DB_screen.getInstance().go_to_query_DB_screen) # no need to grid_forget() when switching to the DB_screen, because if you then go back from there to main_screen, the buttons you should see are the same

            MainScreen_operator.__instance = self



    # the following 3 methods need to be in this class and not in their parent's class because they use an attribute of the class

    def __refill_kits(self):  
        messagebox.showinfo(Language_controller.get_message("efectuar reposicion kits (cabecera)"), Language_controller.get_message("efectuar reposicion kits (cuerpo)"))
        Counters.set_available_kits(constants.AVAILABLE_KITS_AFTER_REFILL)
        self.__remaining_kits_info.config( text = Language_controller.get_message("avisador kits restantes") + str(Counters.get_available_kits()) + Language_controller.get_message("de") + str(constants.AVAILABLE_KITS_AFTER_REFILL), fg = Counters.get_available_kits_fg_color(), bg = Counters.get_available_kits_bg_color())
        DBcontroller.add_new_event( ActivePerson.getCurrent().get_CIP(), "OPERATOR REPLENISHED KITS")
        messagebox.showinfo( Language_controller.get_message("kits repuestos (cabecera)"), Language_controller.get_message("reposicion/recogida finalizada (cuerpo)"))
        # TODO futuro: Que el que hace refill tenga la posibilidad de indicar cuantos AÑADE, por si no llena el deposito entero. En ese caso, el valor de kits será el que había más el añadido

    def __collect_samples(self):
        messagebox.showinfo(Language_controller.get_message("efectuar recogida muestras (cabecera)"), Language_controller.get_message("efectuar recogida muestras (cuerpo)"))
        Counters.set_stored_samples(0)
        self.__stored_samples_info["text"] = Language_controller.get_message("avisador muestras entregadas") + str(Counters.get_stored_samples()) + " (max: " + str(constants.STORED_SAMPLES_LIMIT) +")"
        self.__stored_samples_info["fg"] = Counters.get_stored_samples_fg_color()
        self.__stored_samples_info["bg"] = Counters.get_stored_samples_bg_color()
        DBcontroller.add_new_event( ActivePerson.getCurrent().get_CIP(), "OPERATOR COLLECTED SAMPLES")
        messagebox.showinfo( Language_controller.get_message("muestras recogidas (cabecera)"), Language_controller.get_message("reposicion/recogida finalizada (cuerpo)"))

    def __refill_labels(self):
        messagebox.showinfo(Language_controller.get_message("efectuar reposicion etiquetas (cabecera)"), Language_controller.get_message("efectuar reposicion etiquetas (cuerpo)"))
        Counters.set_available_labels(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL)
        self.__remaining_labels_info.config( text = Language_controller.get_message("avisador etiquetas restantes") + str(Counters.get_available_labels()) + Language_controller.get_message("de") + str(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL), fg = Counters.get_available_labels_fg_color(), bg = Counters.get_available_labels_bg_color() )
        DBcontroller.add_new_event( ActivePerson.getCurrent().get_CIP(), "OPERADOR REPLENISHED LABELS")
        messagebox.showinfo(Language_controller.get_message("etiquetas repuestas (cabecera)"), Language_controller.get_message("reposicion/recogida finalizada (cuerpo)"))


    # changes the texts to the current language. This function is called by Language_controller when a new language is setted
    def change_language(self):
        self.__title["text"] = Language_controller.get_message("título operario")
        self.__logout_b["text"] = Language_controller.get_message("texto botón cerrar sesión para admin/operador")
        self.__quit_program_b["text"] = Language_controller.get_message("apagar")
        self.__refill_kits_b["text"] = Language_controller.get_message("reponer kits")
        self.__refill_labels_b["text"] = Language_controller.get_message("reponer etiquetas")
        self.__collect_samples_b["text"] = Language_controller.get_message("recoger muestras")
        self.__check_DB_b["text"] = Language_controller.get_message("consultar BD")
        # and the language of the information labels don't need to be changed, because the text of those labels is updated each time that the program goes to main screen


    # override abstract parent method
    def go_to_main_screen(self):
        # this is necessary if the mainscreen_operator and mainscreen_admin are already created and an operator has refilled kits / labels or collected samples:
        self.__remaining_kits_info.config( text = Language_controller.get_message("avisador kits restantes") + str(Counters.get_available_kits()) + Language_controller.get_message("de") + str(constants.AVAILABLE_KITS_AFTER_REFILL), fg = Counters.get_available_kits_fg_color(), bg = Counters.get_available_kits_bg_color() )
        self.__remaining_labels_info.config( text = Language_controller.get_message("avisador etiquetas restantes") + str(Counters.get_available_labels()) + Language_controller.get_message("de") + str(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL), fg = Counters.get_available_labels_fg_color(), bg = Counters.get_available_labels_bg_color() )
        self.__stored_samples_info.config( text = Language_controller.get_message("avisador muestras entregadas") + str(Counters.get_stored_samples()) + " (max: " + str(constants.STORED_SAMPLES_LIMIT) +")", fg = Counters.get_stored_samples_fg_color(), bg = Counters.get_stored_samples_bg_color() )

        # column and row configure (because the configuration of the frames is not the same as the user main screen):
        MainScreen._admin_and_operator_header_frame_rowcolumn_configure()
        MainScreen._admin_and_operator_body_frame_rowcolumn_configure()

        # .grids are here and not in constructor because MainScreen_admin, MainScreen_operator and MainScreen_user share the same frame (the main screen frame where this widgets are displayed)
        self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
        self.__logout_b.grid(row = 0, column = 1, sticky = 'NSEW', padx = (10, 5), pady = 10)
        self.__quit_program_b.grid(row = 0, column = 2, sticky = 'NSEW', padx = (5, 10), pady = 10)

        self.__remaining_labels_info.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW', pady = (10,0))
        self.__remaining_kits_info.grid(row = 0, column = 2, columnspan = 2, sticky = 'NSEW', pady = (10,0))
        self.__stored_samples_info.grid(row = 0, column = 4, columnspan = 2, sticky = 'NSEW', pady = (10,0))

        self.__refill_kits_b.grid(row = 1, column = 0, columnspan = 3, sticky = 'NSEW', padx = (10, 5), pady = (10, 5))
        self.__refill_labels_b.grid(row = 1, column = 3, columnspan = 3, sticky = 'NSEW', padx = (5, 10), pady = (10, 5))
        self.__collect_samples_b.grid(row = 2, column = 0, columnspan = 3, sticky = 'NSEW', padx = (10, 5), pady = (5, 10))
        self.__check_DB_b.grid(row = 2, column = 3, columnspan = 3, sticky = 'NSEW', padx = (5, 10), pady = (5, 10))

        MainScreen._main_screen_frame.tkraise()


    # override abstract parent method
    def erase_mainScreen_contents(self):
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

    # override abstract parent method
    def logOut_button(self):
        logout = messagebox.askyesno(Language_controller.get_message("mensaje cierre sesión (cabecera)"), Language_controller.get_message("mensaje cierre sesión (cuerpo)"))
        if logout == True:
            self.erase_mainScreen_contents()
            ActivePerson.getCurrent().logOut()
