from tkinter import *

from Person import ActivePerson
import Screen_manager
import constants
import DBcontroller
import Language_controller


# only admins and users have access to this screen

class Query_DB_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if Query_DB_screen.__instance == None:
            Query_DB_screen()
        return Query_DB_screen.__instance

    def __init__(self):
        if Query_DB_screen.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("Query_BD_screen class is singleton")
        else:
            self.__DBscreen_frame = Screen_manager.init_screen_frame()
            self.__DBscr_header_frame = Screen_manager.header_frame(self.__DBscreen_frame)
            self.__DBscr_body_frame = Screen_manager.body_frame(self.__DBscreen_frame)


            self.__current_DB = "info_uso"

            self.__title = Label(self.__DBscr_header_frame, text = Language_controller.get_message("base de datos:") + self.__current_DB, bg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_TITLE_TEXT_SIZE, 'bold'))
            self.__change_displayed_DB_b = Button(self.__DBscr_header_frame, text = Language_controller.get_message("cambiar de base de datos"), borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__change_displayed_DB)
            self.__return_b = Button(self.__DBscr_header_frame, text = Language_controller.get_message("volver atrás"), borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__change_displayed_DB_b.grid(row = 0, column = 1, sticky = 'NSEW', padx = (10 , 5), pady = 10)
            self.__return_b.grid(row = 0, column = 2, sticky = 'NSEW', padx = (5, 10), pady = 10)

            self.__DBscr_header_frame.columnconfigure(0, weight = 4)
            self.__DBscr_header_frame.columnconfigure(1, weight = 1)
            self.__DBscr_header_frame.columnconfigure(2, weight = 1)
            self.__DBscr_header_frame.rowconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one row in the header_frame) for sticky=NSEW of title and return_b to work correctly


            self.__DB_content_display_box = Text(self.__DBscr_body_frame) 
            self.__scrollbarY = Scrollbar(self.__DBscr_body_frame, orient = "vertical", command = self.__DB_content_display_box.yview)  # associate the yview of my content display to the value of the scrollbar
            self.__DB_content_display_box.config( yscrollcommand = self.__scrollbarY.set ) # associate the scrollbar with my contentdisplay
            self.__fill_display_box_with_DB_content()

            self.__DB_content_display_box.grid(row = 0, column = 0, sticky='NSEW', padx=(20,0), pady=10 )
            self.__scrollbarY.grid(row = 0, column=1, sticky='NSEW', padx=(0,20), pady=10 )

            self.__DBscr_body_frame.columnconfigure(0, weight=29)
            self.__DBscr_body_frame.columnconfigure(1, weight=1)
            self.__DBscr_body_frame.rowconfigure(0, weight = 1)  # it's necessary to give a weight (even though there is only one row in the header_frame) for sticky=NSEW of title and return_b to work correctly
             

            # TODO: Si hay alguna funcionalidad que quieran hacer acerca de la DB, añadir botones con diferentes opciones a la derecha del todo. Por ejemplo la opcion de abajo a la derecha podria permitir ver la otra tabla que no se muestra (esta que sustituya el output de la otra tabla que se está viendo.

            Query_DB_screen.__instance = self


    def __fill_display_box_with_DB_content(self):
        self.__DB_content_display_box['state']=NORMAL
        self.__DB_content_display_box.delete('1.0', END)
        DB_content = DBcontroller.get_DB_content(self.__current_DB)
        self.__DB_content_display_box.insert(INSERT, DB_content)
        self.__DB_content_display_box['state'] = DISABLED # Disabled makes it only readable (otherwise we would see the inputs there!)



    def __previous_screen(self):
        from MainScreen_admin import MainScreen_admin  # declared here to avoid circular dependency
        from MainScreen_operator import MainScreen_operator
        if (ActivePerson.getCurrent().get_status() == "ADMIN"):
            MainScreen_admin.getInstance().go_to_main_screen()
        else:  # OPERATOR
            MainScreen_operator.getInstance().go_to_main_screen()


    def __change_displayed_DB(self):
        if self.__current_DB == "info_uso":
            self.__current_DB = "muestras_saliva"
        else:
            self.__current_DB = "info_uso"
        self.__fill_display_box_with_DB_content()
        self.__title["text"] = Language_controller.get_message("base de datos:") + self.__current_DB


    # changes the texts to the current language. This function is called by Language_controller when a new language is setted
    def change_language(self): 
        self.__change_displayed_DB_b["text"] = Language_controller.get_message("cambiar de base de datos")
        self.__return_b["text"] = Language_controller.get_message("volver atrás")
        # and the language of the title label doesn't need to be changed, because the text of this labels is updated each time that the program goes to main screen 


    def go_to_query_DB_screen(self):
        self.__change_displayed_DB_b["state"] = NORMAL if (ActivePerson.getCurrent().get_status() == "ADMIN") else DISABLED
        self.__current_DB = "info_uso"
        self.__title["text"] = Language_controller.get_message("base de datos:") + self.__current_DB
        self.__fill_display_box_with_DB_content()
        self.__DBscreen_frame.tkraise()

