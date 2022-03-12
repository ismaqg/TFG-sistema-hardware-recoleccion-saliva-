from abc import ABC, abstractmethod

from tkinter import messagebox

from Person import ActivePerson  # to make abstract classes
import Screen_manager
import DBcontroller
import Language_controller

# The idea of ​​this class is that it will contain the frame of the main screen, but 3 classes will inherit from it, which must
# have access to that frame. Those 3 classes that inherit are singleton and when they are instantiated for the first and only time
# they will call the create_main_frame function of their parent.
# That method is a class method, which means that the class atributes (i.e. the frame) will have the same conent for anyone using them. So only
# the first time that create_main_frame is invoked, the frame will be created, and the next times that create_main_frame is invoked, will be ignored
# Children of this class will have access to that frame


class MainScreen(ABC): # abstract

    # class atributes. Protected.
    _main_screen_frame = None
    _ms_header_frame = None
    _ms_body_frame = None

    @classmethod
    def create_main_frames(cls):
        if (cls._main_screen_frame != None):  # check if main screen frame has already been created
            return
        cls._main_screen_frame = Screen_manager.init_screen_frame()
        cls._ms_header_frame = Screen_manager.header_frame(cls._main_screen_frame)
        cls._ms_body_frame = Screen_manager.body_frame(cls._main_screen_frame)

    @classmethod
    def _admin_and_operator_header_frame_rowcolumn_configure(cls):
        cls._ms_header_frame.columnconfigure(0, weight = 4)
        cls._ms_header_frame.columnconfigure(1, weight = 1)
        cls._ms_header_frame.columnconfigure(2, weight = 1)
        cls._ms_header_frame.rowconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one row in ms_header_frame) for sticky=NSEW of the inside widgets to work correctly

    @classmethod
    def _admin_and_operator_body_frame_rowcolumn_configure(cls):
        cls._ms_body_frame.rowconfigure(0, weight = 1)
        cls._ms_body_frame.rowconfigure(1, weight = 4)
        cls._ms_body_frame.rowconfigure(2, weight = 4)
        cls._ms_body_frame.columnconfigure(0, weight = 1)
        cls._ms_body_frame.columnconfigure(1, weight = 1)
        cls._ms_body_frame.columnconfigure(2, weight = 1)
        cls._ms_body_frame.columnconfigure(3, weight = 1)
        cls._ms_body_frame.columnconfigure(4, weight = 1)
        cls._ms_body_frame.columnconfigure(5, weight = 1)

    @classmethod
    def _user_header_frame_rowcolumn_configure(cls):
        cls._ms_header_frame.columnconfigure(0, weight = 4)
        cls._ms_header_frame.columnconfigure(1, weight = 1)
        cls._ms_header_frame.columnconfigure(2, weight = 1)
        cls._ms_header_frame.rowconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one row in ms_header_frame) for sticky=NSEW of the inside widgets to work correctly

    @classmethod
    def _user_body_frame_rowcolumn_configure(cls):
        cls._ms_body_frame.rowconfigure(0, weight = 1)
        cls._ms_body_frame.rowconfigure(1, weight = 0)
        cls._ms_body_frame.rowconfigure(2, weight = 0)
        cls._ms_body_frame.columnconfigure(0, weight = 3)
        cls._ms_body_frame.columnconfigure(1, weight = 3)
        cls._ms_body_frame.columnconfigure(2, weight = 0)
        cls._ms_body_frame.columnconfigure(3, weight = 0)
        cls._ms_body_frame.columnconfigure(4, weight = 0)
        cls._ms_body_frame.columnconfigure(5, weight = 0)
         

    @staticmethod
    def _collect_samples():
        # TODO: mover casi todo el contenido de esta funcion de operator y admin a aqui, y desde allí llamar a esta función. Luego, añadir lo siguiente:
        # - imprimir etiqueta (si esta viva la impresora, si no ya sabes) con la etiqueta ID (formada por ID maquina + numero contenedor)
        # - decirle a admin/operator que ya puede recoger el contenedor y le debe pegar la etiqueta
        # - mover de la BD local a la remota las samples con la funcion esa que tengo del DBcontroller
        # - incrementar el numero de contenedor para la proxima vez que se recojan samples (tiene que ir despues del punto anterior por huevos porque ahí se usa el numero de contenedor)
        # NOTA: al string que representa el evento que se pone en info uso añadirle el ID del contenedor que se esta recogiendo
        pass


    @staticmethod
    def _quit_program():  # only accessible from operator and admin
        shutdown = messagebox.askokcancel(Language_controller.get_message("apagar"), Language_controller.get_message("el programa se cerrará y la máquina se apagará"))
        if shutdown == True:
            DBcontroller.add_new_event( ActivePerson.getCurrent().get_CIP(), "PROGRAM SHUTDOWN" )
            Screen_manager.get_root().destroy()
            # TODO: hacer un shutdown now de la rpi por codigo (y en el bashrc de la rpi hacer que se lance esta aplicacion directamente)    

    @abstractmethod
    def logOut_button(self):
        pass

    @abstractmethod
    def erase_mainScreen_contents(self):
        pass

    @abstractmethod
    def go_to_main_screen(self):
        pass


    