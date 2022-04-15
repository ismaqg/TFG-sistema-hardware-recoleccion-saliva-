from http.client import OK
from tkinter import *
from tkinter import messagebox

from PIL import ImageTk,Image

import time

import Printer_controller
import Screen_manager
import constants
import Checker
from Checker import Priority
import Arduino_controller
import Counters
import DBcontroller
import Language_controller
from Language_controller import Language
from Person import ActivePerson



class SubmitSample_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if SubmitSample_screen.__instance == None:
            SubmitSample_screen()
        return SubmitSample_screen.__instance

    def __init__(self):
        if SubmitSample_screen.__instance != None:
            Screen_manager.get_root().destroy()
            raise Exception("SubmitSample_screen class is singleton")
        else:
            self.__current_step = 1

            self.__submitSampleScreen_frame = Screen_manager.init_screen_frame()
            self.__submitS_header_frame = Screen_manager.header_frame( self.__submitSampleScreen_frame)
            self.__submitS_body_frame = Screen_manager.body_frame( self.__submitSampleScreen_frame)

            self.__title = Label(self.__submitS_header_frame, text = Language_controller.get_message("entregar una muestra"), bg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_TITLE_TEXT_SIZE, 'bold'))
            self.__return_b = Button(self.__submitS_header_frame, text = Language_controller.get_message("volver atrás"), borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__return_b.grid(row = 0, column = 1, sticky = 'NSEW', pady=10, padx=10)

            self.__submitS_header_frame.columnconfigure(0, weight=5)
            self.__submitS_header_frame.columnconfigure(1, weight=1)
            self.__submitS_header_frame.rowconfigure(0, weight=1)  # it's necessary to give a weight (even though there is only one row in clamKitscreen_header_frame) for sticky=NSEW of the inside widgets to work correctly


            self.__info_steps_title = Label(self.__submitS_body_frame, text = Language_controller.get_message("paso número...") + "1", bg = "white", fg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
            self.__info_steps_displayer = Canvas(self.__submitS_body_frame)
            self.__next_step_b = Button(self.__submitS_body_frame, text = Language_controller.get_message("botón siguiente"), borderwidth=3, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__next_step_actions)

            self.__info_steps_title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__info_steps_displayer.grid(row = 1, column = 0, sticky = 'NSEW', padx = 20)
            self.__next_step_b.grid(row = 2, column=0, sticky = 'NSEW', padx=120, pady = 5)

            self.__submitS_body_frame.rowconfigure(0, weight = 1)
            self.__submitS_body_frame.rowconfigure(1, weight = 8)
            self.__submitS_body_frame.rowconfigure(2, weight = 1)
            self.__submitS_body_frame.columnconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one column in clamKitscreen_body_frame) for sticky=NSEW of the inside widgets to work correctly

            SubmitSample_screen.__instance = self


    def __previous_screen(self):
        from MainScreen_user import MainScreen_user  # declared here to avoid circular dependency. It cannot be declared at the beggining of the file cannot be declared at the top of the file or in the constructor
        MainScreen_user.getInstance().go_to_main_screen()


    # TODO: Algunos comentarios de aquí abajo los tendré que cambiar si al final las compuertas no son abiertas y cerradas por un arduino
    """
    STEP 1: Show the first instruction -> Salivate and spit in the big tube. The necessary of this step is done in go_to_submitSample_screen, not in next_step_actions.
    STEP 2: Show the 2nd instruction -> transfer saliva to small tube.
    STEP 3: Says that the next thing will be to print the identifier. The button in this step is "print label" but the printing is done during the next step
    STEP 4: While the printing is being done, this step shows how to stick the label and ask to stick like the image. When the printing has finished, the "next" button is enabled
    STEP 5: Show the next instruction -> Clean the tube. 
    STEP 6: It says to deliver the tube at the gate and press "Entregado" when done. The button is disabled until the door is opened
    STEP 7: It's not a step as such. If we are here we know that all of the above steps have already been completed, so in this point the user will be logged out
    """
    def __next_step_actions(self):

        self.__current_step += 1

        if self.__current_step == 7: # It will be entered here when the user clicks the button of "SAMPLE SUBMITTED". This will mean that the user is saying that has submitted a sample but the arduino hasn't detected it.
            self.__sample_submitted(arduino_detection = False)
            return

        # current step visuals
        self.__info_steps_title["text"] = Language_controller.get_message("paso número...") + str(self.__current_step)
        self.__set_current_step_image()

        # Change the text of the button of this step and make the actions associated, if any:
        if self.__current_step in {2, 5}: 
            self.__next_step_b["text"] = Language_controller.get_message("botón siguiente")
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 3:
            self.__next_step_b["text"] = Language_controller.get_message("botón imprimir etiqueta")
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 4:
            self.__next_step_b["text"] = Language_controller.get_message("botón siguiente")
            self.__next_step_b["state"] = DISABLED
            self.__most_recent_labelID = constants.MACHINE_ID + time.strftime('%d%m%y%H%M%S')  # the labelID is stored in "self" because is used in the "__sample_submitted() function"
            Printer_controller.print_label(self.__most_recent_labelID)
            DBcontroller.add_submission_ID(self.__most_recent_labelID)
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 6:
            self.__next_step_b["text"] = Language_controller.get_message("botón avisar muestra entregada")
            self.__next_step_b["state"] = DISABLED
            Arduino_controller.start_checking_if_sample_submission()
            self.__next_step_b["state"] = NORMAL
            # Program a timer to check if sample was submitted (each 0.5seconds):
            self.__check_is_submitted_countdown = Screen_manager.get_root().after(500, self.__check_if_sample_submitted)

            

    def __set_current_step_image(self):
        current_language = Language_controller.get_current_language()  # return enum
        language_str = current_language.name.lower()  # enum to string (and lowecased)
        img = Image.open(constants.IMAGES_DIRECTORY + "step" + str(self.__current_step) + "_" + language_str + ".png")
        img = img.resize((self.__info_steps_displayer.winfo_width(), self.__info_steps_displayer.winfo_height()), Image.ANTIALIAS)
        self.__current_step_img = ImageTk.PhotoImage( img )  # current_step_img needs to be a class atribute. Otherwise, it won't work
        x_center_canva = int(self.__info_steps_displayer.winfo_width() / 2)
        y_center_canva = int(self.__info_steps_displayer.winfo_height() / 2)
        self.__info_steps_displayer.create_image(x_center_canva, y_center_canva, image = self.__current_step_img)


    def __check_if_sample_submitted(self):
        if (Arduino_controller.is_sample_submitted()):
            self.__sample_submitted(arduino_detection = True)
            # NOTE: Here it's not necessary to call Arduino_controller.stop_checking_if_sample_submission() because Arduino implicitly stops doing that checking if has detected a sample submission.
        else:
            # Reprogram the timer (for another 0.5s):
            self.__check_is_submitted_countdown = Screen_manager.get_root().after(500, self.__check_if_sample_submitted)


    def __sample_submitted(self, arduino_detection):

        self.__next_step_b["state"] = DISABLED
        Counters.increment_stored_samples()
        DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "SAMPLE SUBMITTED")  # to info_uso DB
        DBcontroller.add_sample_submission()  # to muetras_saliva DB. This function implicitly add a temperature (calling the arduino function) and some other important things
        ActivePerson.getCurrent().set_has_submitted_to_true()
        
        if (not arduino_detection): # this function has been called because user indicated the sample submission by clicking the button, but the arduino didn't detect the sample!
            Screen_manager.get_root().after_cancel(self.__check_is_submitted_countdown)  # don't want to go anymore to the "check_if_sample_submitted" function. NOTE: This is only called in the case of "arduino didnt detect", because otherway the timer is not reprogrammed so is not necessary an "after_cancel"
            Checker.notify_operator("User informed of a sample submission but Arduino didn't detect it. The label ID of the sample is: " + self.__most_recent_labelID, Priority.LOW)
            Arduino_controller.stop_checking_if_sample_submission()  #in the Rpi we stopped checking if submitted, but... we need to communicate this (the fact that the user has clicked on SAMPLE SUBMITTED) to the arduino (read arduino code to see why)

        # Show info about sample delivered and log out. If users says OK just log him out, but if user doesn't interact (is AFK) after delivering sample, log him out also! 
        try:
            aux = Tk() # auxiliar screen where show the messagebox
            aux.withdraw() # hide the new auxiliar screen.
            after_identification = aux.after(10000, aux.destroy)  # if user is AFK (10 sec without interacting), destroy the auxiliar screen (and it will destroy the messagebox!)
            messagebox.showinfo(Language_controller.get_message("aviso de muestra entregada (cabecera)"), Language_controller.get_message("aviso de muestra entregada (cuerpo)"), master = aux)  # the parent of this messagebox is the auxiliar screen
            if messagebox.OK: # the user is not AFK, so we need to cancel the timeout, destroy the auxiliar window and logOut (in the 'finally' clause)
                aux.after_cancel(after_identification) 
                aux.destroy()
        except: # si salta el temporizador del after entraremos aquí porque ya no se podrá coger la respuesta del messagebox porque no existirá. El except está creado para que esa excepción no nos salga por pantalla y se ignore.
            pass
        finally: # independientemente de si el usuario ha interactuado o estaba AFK (que en ese caso salta una excepcion despues de destruir la pantalla auxiliar) se deberá hacer logout de la persona (que eso implícitamente devuelve al sistema a la pantalla de logIn)
            ActivePerson.getCurrent().logOut()
            


            
          

    # changes the texts to the current language. This function is called by Language_controller when a new language is setted
    def change_language(self):
        self.__title["text"] = Language_controller.get_message("entregar una muestra")
        self.__return_b["text"] = Language_controller.get_message("volver atrás")
        # the next_step_button and the info_steps_title texts are changed every time that the program changes to this screen 


    def go_to_submitSample_screen(self):
        self.__current_step = 1
        self.__info_steps_title["text"] = Language_controller.get_message("paso número...") + "1"
        self.__set_current_step_image()
        self.__next_step_b["text"] = Language_controller.get_message("botón siguiente")
        self.__next_step_b["state"] = NORMAL
        self.__submitSampleScreen_frame.tkraise()
        messagebox.showwarning(Language_controller.get_message("información previa (cabecera)"), Language_controller.get_message("información previa (recordatorio)"))