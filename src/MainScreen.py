from abc import ABC, abstractmethod  # to make abstract classes
import Screen_manager

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
    def create_main_frame(cls):
        if (cls._main_screen_frame != None):  # check if main screen frame has already been created
            return
        cls._main_screen_frame = Screen_manager.init_screen_frame()
        cls._ms_header_frame = Screen_manager.header_frame(cls._main_screen_frame)
        cls._ms_body_frame = Screen_manager.body_frame(cls._main_screen_frame)

    @abstractmethod
    def go_to_main_screen(self):
        pass

    @abstractmethod
    def logOut(self):
        pass