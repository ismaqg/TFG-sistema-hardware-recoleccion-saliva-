from abc import ABC, abstractmethod

from tkinter import messagebox

from Person import ActivePerson  # to make abstract classes
import Screen_manager
import DBcontroller

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
        cls._ms_header_frame.columnconfigure(0, weight = 5)
        cls._ms_header_frame.columnconfigure(1, weight = 1)
        cls._ms_header_frame.columnconfigure(2, weight = 0)
        cls._ms_header_frame.rowconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one row in ms_header_frame) for sticky=NSEW of the inside widgets to work correctly

    @classmethod
    def _user_body_frame_rowcolumn_configure(cls):
        cls._ms_body_frame.rowconfigure(0, weight = 1)
        cls._ms_body_frame.rowconfigure(1, weight = 1)
        cls._ms_body_frame.rowconfigure(2, weight = 0)
        cls._ms_body_frame.columnconfigure(0, weight = 3)
        cls._ms_body_frame.columnconfigure(1, weight = 3)
        cls._ms_body_frame.columnconfigure(2, weight = 1)
        cls._ms_body_frame.columnconfigure(3, weight = 0)
        cls._ms_body_frame.columnconfigure(4, weight = 0)
        cls._ms_body_frame.columnconfigure(5, weight = 0)
         


    @abstractmethod
    def go_to_main_screen(self):
        pass

    @abstractmethod
    def _erase_mainScreen_contents(self):
        pass


    @staticmethod
    def _quit_program():  # only accessible from operator and admin
        shutdown = messagebox.askokcancel("APAGAR", "El programa se cerrará y la máquina se apagará")
        if shutdown == True:
            DBcontroller.add_new_event( ActivePerson.getCurrent().get_CIP(), "APLICACIÓN APAGADA" )
            Screen_manager.get_root().destroy()
            # TODO: hacer un shutdown now de la rpi por codigo (y en el bashrc de la rpi hacer que se lance esta aplicacion directamente)    

    @abstractmethod
    def logOut_button(self):
        pass


    