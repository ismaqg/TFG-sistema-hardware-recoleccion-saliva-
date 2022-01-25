from tkinter import *
from PIL import ImageTk,Image
import Screen_manager
import constants


class LogIn_screen():  # singleton

    __instance = None

    @staticmethod 
    def getInstance():
        if LogIn_screen.__instance == None:
            LogIn_screen()
        return LogIn_screen.__instance

    def __init__(self):
        if LogIn_screen.__instance != None:
            raise Exception("LogIn_screen class is singleton")
        else:
            self.__input_variable = StringVar() #Tkinter variable

            self.__login_screen_frame = Screen_manager.init_screen_frame()
            self.__login_screen_isActive = False # It is necessary to know when we are in the login tab so that the input is only processed in the login tab, since the function executed in every input is executed in any tab because the input is associated with root. 

            login_title = Label(self.__login_screen_frame, text="Bienvenido a SALIBANK", font = ("Verdana", 28), bg="#7BACFC")
            login_canvas = Canvas(self.__login_screen_frame,  bg="white", highlightthickness=0)
            self.__login_image = ImageTk.PhotoImage(Image.open(constants.IMAGES_DIRECTORY + "TSIdummy.png"))
            login_canvas.create_image(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/4, anchor = CENTER, image = self.__login_image)
            login_info = Label(self.__login_screen_frame, text="Pase su tarjeta sanitaria individual por el lector de código de barras",font = ("Verdana", 14, "bold"), bg="#7BACFC")
            self.__login_input_entry = Entry(self.__login_screen_frame, textvariable = self.__input_variable, borderwidth=0,fg='white', highlightthickness = 0, insertbackground = "white") # invisible
            login_language = Button(self.__login_screen_frame, text="Cambiar Idioma", font = ("Verdana", 12)) # TODO: Añadirle un command=cambiar a la pestaña de idiomas

            login_title.grid(row=0,column=0, columnspan = 2, sticky = 'NSEW')
            login_canvas.grid(row=1, column=0, columnspan = 2, sticky = 'NSEW')
            login_info.grid(row=2, column=0, columnspan = 2, sticky = 'NSEW', pady = (0,10))
            self.__login_input_entry.grid(row=3,column=0, columnspan = 2, sticky = 'NSEW')
            login_language.grid(row=4, column=1, columnspan = 2, sticky = 'NSEW', pady=(10,0))
            self.__login_input_entry.focus_set() # keep the focus on the Entry so that it is ready to receive an input anytime (even if some other widget is clicked)
    
            self.__login_screen_frame.rowconfigure(0,weight=2)
            self.__login_screen_frame.rowconfigure(1,weight=4)
            self.__login_screen_frame.rowconfigure(2,weight=1)
            self.__login_screen_frame.rowconfigure(3,weight=0)
            self.__login_screen_frame.rowconfigure(4,weight=1)

            self.__login_screen_frame.columnconfigure(0,weight=3)
            self.__login_screen_frame.columnconfigure(1,weight=1)

            Screen_manager.get_root().bind('<Return>', self.__process_input) # bind the "enter" key to a function. The barcode reader gives the input in the same way as if it were a keyboard
                                                                            # and at the end the enter key is pressed. Nothing extra is needed to use it. The bind function MUST be used over the root window
            LogIn_screen.__instance = self

    # function to log in the application with the input data (from the barcode scanner). If log in is successful, the user will go to the main screen of the application
    def __try_to_logIn(self):
        #TODO: aparte de todo lo que hay que hacer aqui, añadir a la DB de uso el intento de login (tanto en exito como en fracaso)
        pass

    # function to process the input of the barcode scanner
    def __process_input(self, event):
        if (self.__login_screen_isActive):
            self.__try_to_logIn()
        self.__input_variable.set('')
        self.__login_input_entry.delete(0,'end')

    # function to change the boolean value of the atribute isActive, which indicates if the login screen is the active screen in the application or not. This information is needed by the barcode scanner
    def set_login_screen_isActive(self, bool_isActive):
        self.__login_screen_isActive = bool_isActive

    # function to change the current screen to the login screen
    def go_to_login_screen(self):
        from Screen_saver import Screen_saver  # here to avoid circular dependency! https://agilno.com/why-cyclic-dependency-errors-occur-a-look-into-the-python-import-mechanism/
        self.__login_screen_isActive = True
        self.__login_screen_frame.tkraise()
        Screen_manager.get_root().after(constants.SCREEN_SAVER_BACK_TIMER, Screen_saver.getInstance().go_to_screen_saver)
 

