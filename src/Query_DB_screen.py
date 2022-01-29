from tkinter import *

from Person import ActivePerson
import Screen_manager
import constants
import DBcontroller


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
            raise Exception("Query_BD_screen class is singleton")
        else:
            self.__DBscreen_frame = Screen_manager.init_screen_frame()
            self.__DBscr_header_frame = Screen_manager.header_frame(self.__DBscreen_frame)
            self.__DBscr_body_frame = Screen_manager.body_frame(self.__DBscreen_frame)


            self.__current_DB = "info_uso"

            self.__title = Label(self.__DBscr_header_frame, text = "Base de Datos: " + self.__current_DB, bg = constants.CATSALUT_COLOR, font = ("Verdana", 26, 'bold'))
            self.__change_displayed_DB_b = Button(self.__DBscr_header_frame, text = "Cambiar\nBase de Datos", borderwidth=5, font = ("Verdana", 22, 'bold'), command = self.__change_displayed_DB)
            self.__return_b = Button(self.__DBscr_header_frame, text = "VOLVER", borderwidth=5, font = ("Verdana", 22, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__change_displayed_DB_b.grid(row = 0, column = 1, sticky = 'NSEW', padx = (10 , 5), pady = 20)
            self.__return_b.grid(row = 0, column = 2, sticky = 'NSEW', padx = (5, 10), pady = 20)

            self.__DBscr_header_frame.columnconfigure(0, weight = 4)
            self.__DBscr_header_frame.columnconfigure(1, weight = 1)
            self.__DBscr_header_frame.columnconfigure(2, weight = 1)
            self.__DBscr_header_frame.rowconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one row in the header_frame) for sticky=NSEW of title and return_b to work correctly


            self.__DB_content_display_box = Text(self.__DBscr_body_frame) 
            self.__scrollbarY = Scrollbar(self.__DBscr_body_frame, orient = "vertical", command = self.__DB_content_display_box.yview)  # associate the yview of my content display to the value of the scrollbar
            self.__scrollbarX = Scrollbar(self.__DBscr_body_frame, orient = "horizontal", command = self.__DB_content_display_box.xview)
            self.__DB_content_display_box.config( xscrollcommand = self.__scrollbarX.set, yscrollcommand = self.__scrollbarY.set ) # associate the scrollbar with my contentdisplay
            self.__fill_display_box_with_DB_content()

            self.__DB_content_display_box.grid(row = 0, column = 0, sticky='NSEW', padx=(20,0), pady=(20,0) )
            self.__scrollbarY.grid(row = 0, column=1, sticky='NSEW', padx=(0,20), pady=(20,0) )
            self.__scrollbarX.grid(row = 1, column=0, columnspan=2, sticky='NSEW', padx=20, pady=(0,20) )

            self.__DBscr_body_frame.columnconfigure(0, weight=29)
            self.__DBscr_body_frame.columnconfigure(1, weight=1)
            self.__DBscr_body_frame.rowconfigure(0, weight = 10)
            self.__DBscr_body_frame.rowconfigure(1, weight = 1) 

            # TODO: Si hay alguna funcionalidad que quieran hacer acerca de la DB, añadir botones con diferentes opciones a la derecha del todo. Por ejemplo la opcion de abajo a la derecha podria permitir ver la otra tabla que no se muestra (esta que sustituya el output de la otra tabla que se está viendo.
            # TODO: Si no quieren ninguna funcionalidad más allá de poder ver la otra base de datos, puedo poner el boton de ver la otra BD en el header, al lado del boton de volver
            # TODO: Voy a hacer que admin y operator puedan hacer lo mismo, pero si luego me dicen que operator no pueda hacer X cosas pues solo tengo que poner ese boton en cuestion a disable si es operator. Es decir, al declarar el boton poner algo tipo: state = ActivePerson.getCurrent().getStatus == Operator ? DISABLED : NORMAL.

            Query_DB_screen.__instance = self


    def __fill_display_box_with_DB_content(self):
        self.__DB_content_display_box['state']=NORMAL
        self.__DB_content_display_box.delete(0.0, END)
        DB_content = DBcontroller.get_DB_content(self.__current_DB)
        self.__DB_content_display_box.insert(0.0, DB_content)
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
        self.__title["text"] = "Base de Datos: " + self.__current_DB


    def go_to_query_DB_screen(self):
        self.__change_displayed_DB_b["state"] = NORMAL if (ActivePerson.getCurrent().get_status() == "ADMIN") else DISABLED
        self.__current_DB = "info_uso"
        self.__fill_display_box_with_DB_content()
        self.__DBscreen_frame.tkraise()

