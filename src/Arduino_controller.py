from shutil import which
from tkinter import messagebox

import Checker
import DBcontroller
from Not_available_screen import Not_available_screen
from Person import ActivePerson
import Language_controller
import constants

import serial
import signal
import time


GET_TEMP_IDENTIFIER = '0'
TEMP_STRING_LENGTH = 5

arduino_storage = None
arduino_supply = None


def init_arduinos_connections():
    global arduino_storage, arduino_supply
    arduino_storage = serial.Serial(constants.ARDUINO_STORAGE_PORT, 9600, timeout = constants.ARDUINO_COMMUNICATION_TIMEOUT + 1) # NOTE: if communication needs more than ARDUINO_COMMUNICATION_TIMEOUT seconds, an alarm is triggered (and Not_available_screen is raised), you can see it in other functions as get_deposit_temperature(). This "timeout = constants.ARDUINO_COMMUNICATION_TIMEOUT + 1" is here to close the communication with arduino after that happens, to not have blocked the serial communication port trying to still communicate when the program is already inoperative.
    arduino_supply = serial.Serial(constants.ARDUINO_SUPPLY_PORT, 9600, timeout = constants.ARDUINO_COMMUNICATION_TIMEOUT + 1) 
    time.sleep(2); # TODO: Igual puedo ahorrarmela si ya de por sí pasan almenos 2 segundos entre la llamda a esta función y que se intenta establecer la primera comunicación con los arduinos


def inoperative_arduino_actions(which_arduino):
    Checker.notify_operator("ARDUINO (" + which_arduino + ") INOPERATIVO", Checker.Priority.CRITICAL)
    DBcontroller.add_new_event("-", "APP CLOSED. ARDUINO (" + which_arduino + ") INOPERATIVE")
    messagebox.showerror(Language_controller.get_message("error recogida kit (cabecera)"), Language_controller.get_message("error recogida kit (cuerpo)"))  
    ActivePerson.getCurrent().logOut()
    Not_available_screen.getInstance().go_to_Not_available_screen_screen()


# ignore the 2 parameters of the function. Are send by the signal when SIGALARM triggers but are not used.
def arduino_storage_timeout(signum, sigframe):
    inoperative_arduino_actions("storage")

# ignore the 2 parameters of the function. Are send by the signal when SIGALARM triggers but are not used.
def arduino_supply_timeout(signum, sigframe):
    inoperative_arduino_actions("supply")


def get_deposit_temperature():
    if(Checker.is_arduino_storage_alive): # TODO: Probablemente este if sobra, depende de si en is_arduino_storage_alive solo miro si existe el /dev pertinente o pruebo a comunicarme con él. En caso de que ahí pruebe a comunicarme es tontería tener este if, porque aquí dentro ya intento comunicarme con timeout por si peta!! 
        # ask for temperature to arduino:
        arduino_storage.write(str.encode(GET_TEMP_IDENTIFIER)) 
        # prepare a timeout if label doesn't respond:
        signal.signal(signal.SIGALRM, arduino_storage_timeout)
        signal.alarm(constants.ARDUINO_COMMUNICATION_TIMEOUT)
        # get temperature from arduino:
        temperature = arduino_storage.read(TEMP_STRING_LENGTH).decode('UTF-8') # receive temperature
        # ignore the timeout because if this line is reached, the communication has been done:
        signal.alarm(0)
        # return temperature (string):
        return temperature
    else:
        inoperative_arduino_actions("storage")


""" IMPORTANTE: LEE ESTE TODO DE ABAJO """
# TODO: Creo que sería mejor que se pudiesen llamar tal cual a las funciones de Arduino_controller y que se hiciese allí dentro toda la gestión que hay que hacer si arduino está inoperativo. O sea, que sea dentro de esta clase donde se llame a Checker.is_arduino_alive(), la gestión de timeouts y el salto a NotAvailableScreen.