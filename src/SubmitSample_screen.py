from tkinter import *
from tkinter import messagebox

import barcode   
from barcode.writer import ImageWriter
from barcode import generate

from brother_ql.conversion import convert  
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

from PIL import Image

import time
import signal

import Screen_manager
import constants
import Checker
import Arduino_controller
import Counters
import DBcontroller
import Language_controller
from Person import ActivePerson
from Not_available_screen import Not_available_screen

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

        if self.__current_step == 7: # It will be entered here when the action of the last step (step 6: deliver the sample) has been completed (i.e. THE SAMPLE HAS BEEN SUBMITTED)
            self.__sample_submitted()

        self.__info_steps_title["text"] = Language_controller.get_message("paso número...") + str(self.__current_step)
        # TODO: Añadir la imagen del step que toque al canva al canva (tranquilo que no hay que hacer 6 ifs. A las imagenes las voy a llamar step1, step2, etc. Por lo que puedo conseguir la imagen que toca porque sé el valor de current_step)

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
            self.__print_label()
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 6:
            # TODO: Hay que mirar con el sensor del arduino si de verdad abre la puerta. Timeouts por si peta
            self.__next_step_b["text"] = Language_controller.get_message("botón avisar muestra entregada")
            self.__next_step_b["state"] = DISABLED
            self.__next_step_b["state"] = NORMAL
        

    def __sample_submitted(self):
        if (Checker.is_arduino_storage_alive()):  

            # TODO: Al final parece que usaremos el arduino a modo de sensor de que se haya entregado o para medir la temperatura. Así que poner ese código aquí dentro. OJO: Esta es la función de sample submitted, a
            # la que se supone que llama cuando ya ha cerrado la puerta, así que posiblemente necesito otra función para mirar si se abre la puerta. O MEJOR: ese codigo de ver si se abre la puerta y tal ponerlo en el arduino que
            #vaya mirando siempre, y luego en esta función consultarle al arduino: Oye, realmente ya abrió y cerró la puerta?. Y si no, si tengo que poner el codigo en este fichero, el lugar correcto sería el step 6, no esta función (que se llama en step 8)
            # TODO: Poner timeouts en todas las comunicaciones con el arduino

            Counters.increment_stored_samples()
            DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "SAMPLE SUBMITTED")  # to info_uso DB
            DBcontroller.add_sample_submission()  # to muetras_saliva DB
            ActivePerson.getCurrent().set_has_submitted_to_true()
            messagebox.showinfo(Language_controller.get_message("aviso de muestra entregada (cabecera)"), Language_controller.get_message("aviso de muestra entregada (cuerpo)"))
            ActivePerson.getCurrent().logOut()

            # TODO: Apagar leds de la puerta que ya ha cerrado. Con timeouts por si el arduino falla   
        else:
            Arduino_controller.inoperative_arduino_actions()


    def __print_label(self):
        
        if Checker.is_printer_alive() and Counters.get_available_labels() >= 1:

            #labelID = self.__generate_label_ID() <- TODO para versión final (no prototipo) en funcion de si puedan haber submissions simultaneas, de hw disponible y demás
            labelID = time.strftime('%d%m%y%H%M%S')  # TODO: En la version final (no prototipo) no estará esta línea, sino la de abajo
            
            # generate the barcode (the barcode code will be the labelID variable)
            barcode_class = barcode.get_barcode_class('code128')
            my_barcode = barcode_class(labelID, writer=ImageWriter())
            my_barcode.save(constants.IMAGES_DIRECTORY + 'barcode')  # save the barcode generated as barcode.png

            # open the image with the barcode and resize the printed barcode to make the barcode smaller
            bardcode_img = Image.open(constants.IMAGES_DIRECTORY + 'barcode.png')
            bardcode_img = bardcode_img.resize((991,306))

            # prepare the information to send to the printer (https://stackoverflow.com/questions/55521301/printing-label-from-brother-ql-800-label-printer):
            backendID = 'linux_kernel'    # the possibilities are 'pyusb', 'linux_kernel' or 'network'. But we use linux_kernel because is the simpliest if our Rpi uses a linux kernel (which is the case).
            printer_model = 'QL-700' # your printer model.
            
            qlr = BrotherQLRaster(printer_model)
            qlr.exception_on_warning = True

            print_instructions = convert( # convert an image to a raster instruction file
                qlr=qlr, 
                images=[bardcode_img],    # the image to print.
                label='62',         # Corresponding label, this is the label identifier (62 means that is a we are using labels of width=62). You can find all
                                    # the available labels with the command brother_ql info labels (what you see in the name column is the identifier, in this case, 62).
                                    # And in this link you can find all the attributes associated with each kind of label: https://brother-ql.net/_modules/brother_ql/labels.html#LabelsManager (ver donde pone ALL_LABELS y ahí dentro 
                rotate='auto',    # 'Auto', '0', '90', '270'
                threshold=70.0,    # Black and white threshold in percent.
                dither=False, 
                compress=False, 
                red=False,    # Only True if using Red/Black 62 mm label tape.
                dpi_600=False, 
                lq=False,    # True for low quality.
                no_cut=False
            )
            
            # prepare a timeout if label doesn't respond:
            signal.signal(signal.SIGALRM, self.__printer_not_responding_while_printing)
            signal.alarm(constants.LABEL_PRINTING_TIMEOUT)

            # send the information to the printer:
            send(instructions=print_instructions, printer_identifier=constants.PRINTER_PORT, backend_identifier=backendID, blocking=True)
                
            # ignore the timeout because if this line is reached, the printer has just printed.
            signal.alarm(0)

            DBcontroller.add_new_event("-", "Printed: " + labelID)
            DBcontroller.add_submission_ID(labelID)
            Counters.decrement_available_labels()
            
        else:
            self.__printer_not_responding_while_printing(None, None)
            

    @staticmethod
    def __printer_not_responding_while_printing(signum, frame):
        messagebox.showerror(Language_controller.get_message("aviso de error de impresión (cabecera)"), Language_controller.get_message("aviso de error de impresión (cuerpo)"))
        Checker.notify_operator("Impresora colgada a media impresión", Checker.Priority.CRITICAL)
        if Counters.get_available_labels() >= 1:
            DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "USER DISCONECTED: PRINTER NOT WORKING")
        else:
            DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "USER DISCONECTED: NON AVAILABLE LABELS")
        ActivePerson.getCurrent().logOut()
        Not_available_screen.getInstance().go_to_Not_available_screen_screen()

    """
    TODO: Comentar a profe que con la grandaria de nuestras etiquetas y precisión de nuestro lector de barras, es imposible hacer un codigo de barras unico (formado a partir del tiempo actual y del CIP del usuario) que sea leible por el lector. Por tanto, lo haré solo en base al tiempo actual (ya que no pueden haber submissions simultaneas) y habrá que poner en la memoria que para la versión final hay que encontrar otro método o tener mejor impresora
    # to be unique, the ID needs time + CIP (encripted CIP for privacy. But not encripted with hash or something that can have collissions). The time is important because the same person can submit different samples, and the CIP is important because if this machine exists in more than 1 place, it is possible tu submit more than one sample in the same instant
    def __generate_label_ID(self):
        CIP_unencripted = ActivePerson.getCurrent().get_CIP()
        CIP_encripted = "" 
        for character in CIP_unencripted:
            if character.isdigit():
                char_to_add = chr( ord(character) - 13)
                if char_to_add == "'":
                    char_to_add = "~"
                CIP_encripted += char_to_add
            else: #is letter
                char_to_add = chr( ord(character) - 30)
                if char_to_add == "'":
                    char_to_add = "~"
                CIP_encripted += char_to_add
        return time.strftime('%d%m%y%H%M%S') + CIP_encripted
    """
          

    # changes the texts to the current language. This function is called by Language_controller when a new language is setted
    def change_language(self):
        self.__title["text"] = Language_controller.get_message("entregar una muestra")
        self.__return_b["text"] = Language_controller.get_message("volver atrás")
        # the next_step_button and the info_steps_title texts are changed every time that the program changes to this screen 


    def go_to_submitSample_screen(self):
        self.__current_step = 1
        # TODO: Añadir la imagen del step 1 al canva
        self.__next_step_b["text"] = Language_controller.get_message("botón siguiente")
        self.__next_step_b["state"] = NORMAL
        self.__info_steps_title["text"] = Language_controller.get_message("paso número...") + "1"
        self.__submitSampleScreen_frame.tkraise()
        messagebox.showwarning(Language_controller.get_message("información previa (cabecera)"), Language_controller.get_message("información previa (recordatorio)"))