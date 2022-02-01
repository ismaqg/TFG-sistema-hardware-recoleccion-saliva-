from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

import Screen_manager
import constants
import DBcontroller
import Checker
from Person import ActivePerson
from MainScreen_admin import MainScreen_admin
from MainScreen_operator import MainScreen_operator
from MainScreen_user import MainScreen_user
from Key_security import Key_security
from Language_screen import Language_screen



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

            self.__login_screen_isActive = False  # It is necessary to know when we are in the login tab so that the input is only processed in the login tab, since the function executed in every input is executed in any tab because the input is associated with root. 
            self.__saver_countdown = None  # Identifies the inactivity countdown used to redisplay the screensaver. For the moment, is invalid, until the first countdown is started in the "go_to_login_screen" function.

            self.__login_screen_frame = Screen_manager.init_screen_frame()            

            login_title = Label(self.__login_screen_frame, text="Bienvenido a SALIBANK", font = (constants.CATSALUT_TEXT_FONT, 28, 'bold'), bg = constants.CATSALUT_COLOR)
            login_canvas = Canvas(self.__login_screen_frame,  bg="white", highlightthickness=0)
            self.__login_image = ImageTk.PhotoImage(Image.open(constants.IMAGES_DIRECTORY + "TSIdummy.png"))
            login_canvas.create_image(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/4, anchor = CENTER, image = self.__login_image)
            login_info = Label(self.__login_screen_frame, text="Pase su tarjeta sanitaria individual por el lector de código de barras",font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_THIRD_TITLE_TEXT_SIZE, "bold"), bg = constants.CATSALUT_COLOR)
            self.__login_input_entry = Entry(self.__login_screen_frame, textvariable = self.__input_variable, borderwidth=0,fg='white', highlightthickness = 0, insertbackground = "white") # invisible
            self.__change_language = Button(self.__login_screen_frame, text="Cambiar Idioma", font = (constants.CATSALUT_TEXT_FONT, constants.SECONDARY_BUTTON_TEXT_SIZE), command = Language_screen.getInstance().go_to_language_screen) 

            login_title.grid(row=0,column=0, columnspan = 2, sticky = 'NSEW')
            login_canvas.grid(row=1, column=0, columnspan = 2, sticky = 'NSEW')
            login_info.grid(row=2, column=0, columnspan = 2, sticky = 'NSEW', pady = (0,10))
            self.__login_input_entry.grid(row=3,column=0, columnspan = 2, sticky = 'NSEW')
            self.__change_language.grid(row=4, column=1, columnspan = 2, sticky = 'NSEW', pady=(10,0))
            self.__login_input_entry.focus_set() # keep the focus on the Entry so that it is ready to receive an input anytime (even if some other widget is clicked)
    
            # wheight to each row and column is used to set the proportion that each element occupies with respect to the screen:
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

        # discard the inactivity countdown, because an interaction with a user has just occurred:
        Screen_manager.get_root().after_cancel(self.__saver_countdown)

        #check if the input belongs to a catalan health card or not:
        if (LogIn_screen.__is_a_valid_TSI(self.__input_variable.get())):

            person = ActivePerson(self.__input_variable.get()[6:20]) # In the 'person' class, the distinction as to whether it is admin, operator or user is made

            self.__login_input_entry.delete(0,'end')
            self.__input_variable.set('')

            if person.get_status() == "ADMIN" or person.get_status() == "OPERATOR":
                additional_security_check = Key_security()
                self.__change_language["state"]= DISABLED  # disable the change language button while the key_security_screen is being showed
                # Program a timer to check the response to the 2nd authentication password and logIn (go to main screen) if correct or abort if not correct:
                Screen_manager.get_root().after(500, lambda:self.__check_2nd_authentication_response_and_logIn_if_correct(additional_security_check, person))

            else: # USER
                if Checker.check_available_resources_at_user_logIn() == False:  # cannot login because there are not available resources
                    # NOTE: the function "check available resources at user login" implicitly sends a message of the error to an Operator, and registers the event in the DB.
                    ActivePerson.destroyCurrent()
                    messagebox.showerror("NO PUEDE INICIAR SESIÓN", "No puede iniciar sesión por problemas internos. Vuelva a probarlo en un rato. Los operarios ya están avisados de los problemas y la máquina se apagará cuando pulse sobre 'OK'")
                    # the program (and Rpi) will shut down because inavailability of resources is a critical problem. The operator that comes to solve the problem will turn on the Rpi again:
                    Screen_manager.get_root().destroy() # TODO: At the Rpi change this line by a shutdown
                else:
                    DBcontroller.add_new_event(person.get_CIP(), "USER LOGIN SUCCESS")
                    self.__login_screen_isActive = False  # we are about to leave login screen
                    MainScreen_user.getInstance().go_to_main_screen() 
            
            """
            IMPORTANT:
            Since I don't have access to the catsalut database, any barcode with the correct format is interpreted as an existing user.
            But here a check should also be made to see if the CIP exists in the user catsalut database and, if it does not exist, it should be
            registered in the 'info_uso' database as LOGIN FAILED. Also a warning indicating that the CIP is invalid should be shown on the screen to the user
            and the __login_screen_isActive must be set to false and the saver (inactivity) countdown must restart.
            """ 

        else:
            DBcontroller.add_new_event(self.__input_variable.get(), "INVALID LOGIN")
            self.__login_input_entry.delete(0,'end')
            self.__input_variable.set('')
            messagebox.showwarning("IDENTIFICACIÓN ERRÓNEA", "Por favor, identifíquese con su tarjeta sanitaria individual")
            # start again the inactivity countdown:
            from Screen_saver import Screen_saver  # here to avoid circular dependency!
            self.__saver_countdown = Screen_manager.get_root().after(constants.SCREEN_SAVER_BACK_TIMER, Screen_saver.getInstance().go_to_screen_saver)            

        

    # function to process the input of the barcode scanner
    def __process_input(self, event):

        if (self.__login_screen_isActive and not ActivePerson.thereIsActivePerson()):  # the first condition will only allow inputs from the login screen (for example, dont will allow from the screensaver).
                                                                                  # And the 2nd condition it is there to avoid possible future bugs that may appear between the first and second identification of admins / operators, because there they are in the logIn screen but we really don't want to be able to read inputs
            self.__try_to_logIn()
        
        else: # in the try_to_logIn function those 2 lines below are executed. This else is necessary so that these lines are not executed when the program tries to login and cannot login due to lack of resources (in that case, the program is closed). If not, an exception would be thrown.
            self.__input_variable.set('')
            self.__login_input_entry.delete(0,'end')


    # function to check if a given string is a valid TSI code
    @staticmethod
    def __is_a_valid_TSI(string_to_check):
        if len(string_to_check) != 24:
            return False
        if not string_to_check[0:6].isdigit() or not string_to_check[10:24].isdigit():
            return False
        if not string_to_check[6:10].isalpha():
            return False
        if string_to_check[0:6] != "803401": #catsalut TSI starts with this numbers
            return False
        if int(string_to_check[13:15]) > 12 or int(string_to_check[13:15]) == 0 or int(string_to_check[15:17]) > 31 or int(string_to_check[15:17]) == 0: # string_to_check[13:15] represents a month and string_to_check[15:17] represents a day
            return False
        return True

    # only operators / admins in this function
    def __check_2nd_authentication_response_and_logIn_if_correct(self, additional_security_check, person):
        if (not additional_security_check.key_introduced()):
            # program to check the key input after another 0.5 seconds:
            Screen_manager.get_root().after(500, lambda:self.__check_2nd_authentication_response_and_logIn_if_correct(additional_security_check, person))
        elif (additional_security_check.password_is_correct()):
            self.__change_language["state"]= NORMAL  # enable the change language button for the next time for the next time the user screen is reached
            self.__login_screen_isActive = False  # the authentication has been successful, so we are about to exit the login screen
            if person.get_status() == "ADMIN": 
                DBcontroller.add_new_event(person.get_CIP(), "ADMIN LOGIN SUCCESS")
                MainScreen_admin.getInstance().go_to_main_screen()
            else: # Operator
                DBcontroller.add_new_event(person.get_CIP(), "OPERATOR LOGIN SUCCESS")
                MainScreen_operator.getInstance().go_to_main_screen()
        else:
            self.__change_language["state"]= NORMAL  # enable the change language button
            DBcontroller.add_new_event(person.get_CIP(), person.get_status() + " LOGIN FAIL. WRONG SECURITY PASSWORD")
            ActivePerson.destroyCurrent()  # destroy current admin / operator. (a current admin / operator was created when the 1st identification step succeed, but the 2nd step has failed) 
            messagebox.showwarning("ACCESO DENEGADO", "Acceso erróneo. Por favor, vuelva a intentar acreditarse escaneando su tarjeta e introduciendo la clave numérica correcta")
            # start again the inactivity countdown (to show again the saver):
            from Screen_saver import Screen_saver  # here to avoid circular dependency!
            self.__saver_countdown = Screen_manager.get_root().after(constants.SCREEN_SAVER_BACK_TIMER, Screen_saver.getInstance().go_to_screen_saver) 


    # function to change the boolean value of the atribute isActive, which indicates if the login screen is the active screen in the application or not. This information is needed by the barcode scanner
    def set_login_screen_isActive(self, bool_isActive):
        self.__login_screen_isActive = bool_isActive

    # function to change the current screen to the login screen
    def go_to_login_screen(self):
        self.__login_screen_isActive = True
        self.__login_screen_frame.tkraise()
        # inactivity countdown (if SCREEN_SAVER_BACK_TIMER milliseconds elapse without there having been any input in the login screen, it returns to the saver screen) :
        from Screen_saver import Screen_saver  # here to avoid circular dependency! https://agilno.com/why-cyclic-dependency-errors-occur-a-look-into-the-python-import-mechanism/
        self.__saver_countdown = Screen_manager.get_root().after(constants.SCREEN_SAVER_BACK_TIMER, Screen_saver.getInstance().go_to_screen_saver) 

