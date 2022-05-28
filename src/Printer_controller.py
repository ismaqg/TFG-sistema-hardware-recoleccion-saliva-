from tkinter import messagebox
import constants
import Counters
import Checker
import DBcontroller
import Language_controller
from Not_available_screen import Not_available_screen
from Person import ActivePerson


import barcode   
from barcode.writer import ImageWriter
from barcode import generate

from brother_ql.conversion import convert  
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

from PIL import Image

import time
import signal




def print_label(labelID):

    if Checker.is_printer_alive() and Counters.get_available_labels() >= 1:  

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
        signal.signal(signal.SIGALRM, __printer_not_responding_while_printing)
        signal.alarm(constants.LABEL_PRINTING_TIMEOUT)
        
        # send the information to the printer: TODO: descomentar para Rpi
        send(instructions=print_instructions, printer_identifier=constants.PRINTER_PORT, backend_identifier=backendID, blocking=True)
                    
        # ignore the timeout because if this line is reached, the printer has just printed.
        signal.alarm(0)

        DBcontroller.add_new_event("-", "Printed: " + labelID)
        Counters.decrement_available_labels()
        
    else:
        __printer_not_responding_while_printing(None, None)



# ignore the 2 parameters of the function. Are send by the signal when SIGALARM triggers but are not used.
# This function can be called for this reasons: printer not working or no labels left to print
def __printer_not_responding_while_printing(signum, frame):
    messagebox.showerror(Language_controller.get_message("aviso de error de impresión (cabecera)"), Language_controller.get_message("aviso de error de impresión (cuerpo)"))
    Checker.notify_operator("Impresora no puede usarse (no funciona o faltan etiquetas)", Checker.Priority.CRITICAL)
    if Counters.get_available_labels() >= 1:
        DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "CURRENT SESSION CLOSED: PRINTER NOT WORKING")
    else:
        DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "CURRENT SESSION CLOSED: NON AVAILABLE LABELS")
    ActivePerson.getCurrent().logOut()
    Not_available_screen.getInstance().go_to_Not_available_screen_screen()