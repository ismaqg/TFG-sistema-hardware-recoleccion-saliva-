
from tkinter import messagebox

import Screen_manager
import Checker
import DBcontroller
from Not_available_screen import Not_available_screen
from Person import ActivePerson
import Language_controller
import constants
import time

import serial



# Constants for the arduino STORAGE:
GET_TEMP_IDENTIFIER = '0'
START_CHECKING_IF_SAMPLE_SUBMITTED_IDENTIFIER = '1'
GET_IF_SAMPLE_SUBMITTED_IDENTIFIER = '2'
STOP_CHECKING_IF_SAMPLE_SUBMITTED_IDENTIFIER = '3'
TEMP_STRING_LENGTH = 5
SAMPLE_SUBMISSION_RESPONSE_LENGTH = 1

# Constants for the arduino SUPPLY:
DROP_KIT_IDENTIFIER = '0'  # no pasa nada por que coincida con el GET_TEMP_IDENTIFIER, porque es para otro arduino.
DROP_KIT_FINISHED_SUCCESS = '1'  # kit ha caido y sensor lo ha detectado (y el motor ha parado)
DROP_KIT_FINISHED_FAILURE = '2'  # el sensor no ha detectado caida kit así que el motor ha parado por un timeout programado en el arduino. (puede significar sensor roto o cualquier cosa peor, como que el tornillo sin fin se haya desencajado del motor)
DROP_KIT_RESPONSE_LENGTH = 1
WHO_ARE_YOU_IDENTIFIER = '?'
ARDUINO_ID_RESPONSE_LENGTH = 1
ARDUINO_SUPPLY_ID = 'A'
ARDUINO_STORAGE_ID = 'B'

# Arduino pySerial instances:
arduino_storage = None
arduino_supply = None


# NOTE: Arduino communications have timeouts.
def init_arduinos_connections():
    global arduino_storage, arduino_supply
    if Checker.is_arduino_storage_alive() and Checker.is_arduino_supply_alive():
        arduino_storage = serial.Serial(constants.ARDUINO_STORAGE_PORT, 9600, timeout = constants.ARDUINO_STORAGE_COMMUNICATION_TIMEOUT, write_timeout = constants.ARDUINO_STORAGE_COMMUNICATION_TIMEOUT)
        arduino_supply = serial.Serial(constants.ARDUINO_SUPPLY_PORT, 9600, timeout = constants.ARDUINO_SUPPLY_COMMUNICATION_TIMEOUT, write_timeout = constants.ARDUINO_SUPPLY_COMMUNICATION_TIMEOUT) 
        time.sleep(2) #este es mas o menos el tiempo que necesitan las lineas anteriores para hacerse correctamente antes de que se intente hacer nada de linea serie sobre el arduino. 
    else:
        inoperative_arduino_actions("storage and supply", "No se detecta algún arduino conectado")


# se ocupa de que, si se ha conectado el arduino supply en ACM1 y storage en ACM0 (es decir, al reves de como deberia), actualizar el valor de las variables que contienen la información de los puertos y volver a establecer conexión
def give_correct_port_to_arduinos():
    global arduino_storage, arduino_supply
    if Checker.is_arduino_storage_alive() and Checker.is_arduino_supply_alive():

        # ask for identifier to the arduino connected to the ARDUINO_SUPPLY port:
        try:
            arduino_supply.write(str.encode(WHO_ARE_YOU_IDENTIFIER))
        except:  # SerialTimeoutException (raised if communication timeout is reached)
            inoperative_arduino_actions("supply or storage", "SerialTimeoutException al preguntar al arduino conectado a ACM0 quién es él (si supply o storage")

        # get response (identifier) from arduino:
        arduino_identifier = arduino_supply.read(ARDUINO_ID_RESPONSE_LENGTH).decode('UTF-8')
        if (len(arduino_identifier) != ARDUINO_ID_RESPONSE_LENGTH):  # this will be the case of communication timeout reached
            inoperative_arduino_actions("supply or storage", "ha saltado timeout de comunicacion al intentar recibir el identificador de los arduinos")

        # check if in the ARDUINO_SUPPLY_PORT was connected the ARDUINO_STORAGE (in that case, change the ports of the variables that are indicating each path) and restart the communications (because maybe different timeouts were setted in the init_connections function)
        if arduino_identifier == ARDUINO_STORAGE_ID:
            # swap:
            aux = constants.ARDUINO_SUPPLY_PORT
            constants.ARDUINO_SUPPLY_PORT = constants.ARDUINO_STORAGE_PORT
            constants.ARDUINO_STORAGE_PORT = aux
            # restart serial comm:
            arduino_storage = serial.Serial(constants.ARDUINO_STORAGE_PORT, 9600, timeout = constants.ARDUINO_STORAGE_COMMUNICATION_TIMEOUT, write_timeout = constants.ARDUINO_STORAGE_COMMUNICATION_TIMEOUT)
            arduino_supply = serial.Serial(constants.ARDUINO_SUPPLY_PORT, 9600, timeout = constants.ARDUINO_SUPPLY_COMMUNICATION_TIMEOUT, write_timeout = constants.ARDUINO_SUPPLY_COMMUNICATION_TIMEOUT) 
        elif arduino_identifier == ARDUINO_SUPPLY_ID:
            pass
        else:
            print("ha habido algún problema al mirar quién es el arduino conectado en ACM0: no han retornado ni una 'A' ni una 'B'")

    else:
        inoperative_arduino_actions("storage and supply", "No se detecta algún arduino conectado")


def inoperative_arduino_actions(which_arduino, extra_info):
    Checker.notify_operator("ARDUINO (" + which_arduino + ") INOPERATIVO. Info extra: " + extra_info, Checker.Priority.CRITICAL)
    DBcontroller.add_new_event("-", "APP CLOSED. ARDUINO (" + which_arduino + ") INOPERATIVE")
    messagebox.showerror(Language_controller.get_message("error recogida kit (cabecera)"), Language_controller.get_message("error recogida kit (cuerpo)"))
    if ActivePerson.isThereActivePerson():
        ActivePerson.getCurrent().logOut()
    Not_available_screen.getInstance().go_to_Not_available_screen_screen()


""" ******************* ARDUINO STORAGE FUNCTIONS: ******************* """


def get_deposit_temperature():
    if(Checker.is_arduino_storage_alive()):

        # ask for temperature to arduino:
        try:
            arduino_storage.write(str.encode(GET_TEMP_IDENTIFIER))
        except:  # SerialTimeoutException (raised if communication timeout is reached)
            inoperative_arduino_actions("storage", "SerialTimeoutException al pedir al arduino la temperatura")  

        # get response (temperature) from arduino:
        temperature = arduino_storage.read(TEMP_STRING_LENGTH).decode('UTF-8') # receive temperature
        if (len(temperature) != TEMP_STRING_LENGTH):  # this will be the case of communication timeout reached
            inoperative_arduino_actions("storage", "ha saltado timeout de comunicacion al intentar recibir del arduino la temperatura")

        # return temperature (string):
        return temperature

    else:
        inoperative_arduino_actions("storage", "No se detecta el arduino conectado")


# Check temperature and update DB if needed. After that, a periodic interruption is programmed every X minutes to get the temperature again and repeat the process. 
def get_deposit_temperature_periodically_and_update_DB():
    temperature_str = get_deposit_temperature()
    DBcontroller.modify_DB_temperatures_if_needed(temperature_str)
    Screen_manager.get_root().after(constants.CHECK_TEMPERATURE_TIMER, get_deposit_temperature_periodically_and_update_DB)



def start_checking_if_sample_submission():
    if(Checker.is_arduino_storage_alive()): 
        # say to arduino to start checking if sample is submitted:
        try:
            arduino_storage.write(str.encode(START_CHECKING_IF_SAMPLE_SUBMITTED_IDENTIFIER))
        except:  # SerialTimeoutException (raised if communication timeout is reached)
            inoperative_arduino_actions("storage", "SerialTimeoutException al decir al arduino que puede empezar la comprobación de si se entrega muestra") 
    else:
        inoperative_arduino_actions("storage", "No se detecta el arduino conectado")


# PRE: start_checking_if_sample_submissions() needs to be called before start calling repeteadly this function (for each user)
def is_sample_submitted():
    if(Checker.is_arduino_storage_alive()): 
        
        # ask if sample was submitted to arduino:
        try:
            arduino_storage.write(str.encode(GET_IF_SAMPLE_SUBMITTED_IDENTIFIER))
        except:  # SerialTimeoutException (raised if communication timeout is reached)
            inoperative_arduino_actions("storage", "SerialTimeoutException al pedirle al arduino que nos diga si se entrega muestra")
         
        # get response from arduino ('1' if sample submitted, '0' if not):
        sample_submission_response = arduino_storage.read(SAMPLE_SUBMISSION_RESPONSE_LENGTH).decode('UTF-8')
        if (len(sample_submission_response) != SAMPLE_SUBMISSION_RESPONSE_LENGTH):  # this will be the case of communication timeout reached
            inoperative_arduino_actions("storage", "ha saltado timeout de comunicacion al intentar recibir del arduino la respuesta de si ya se ha detectado una muestra")
        
        # return if sample submitted (boolean):
        return bool(int(sample_submission_response))  # sample_submission_response can be '0' or '1'. And we convert it in true or false
    
    else:
        inoperative_arduino_actions("storage", "No se detecta el arduino conectado")
        return False


# This function will only be called if user indicates that he has submitted a sample and the arduino sensor didn't detect it.
def stop_checking_if_sample_submission():
    if(Checker.is_arduino_storage_alive()): 
        # say to arduino to stop checking if sample is submitted:
        try:
            arduino_storage.write(str.encode(START_CHECKING_IF_SAMPLE_SUBMITTED_IDENTIFIER))
        except:  # SerialTimeoutException (raised if communication timeout is reached)
            inoperative_arduino_actions("storage", "SerialTimeoutException al decir al arduino que ya puede dejar de mirar si se entrega muestra") 
    else:
        inoperative_arduino_actions("storage", "No se detecta el arduino conectado")


""" ******************* ARDUINO SUPPLY FUNCTIONS: ******************* """


# Si el sensor no detecta que cae un kit/ ha habido problemas con el motor o tornillo sin fin, se mostrará la pantalla de not available. Returns true if success, false if not
def drop_kit():
    if(Checker.is_arduino_supply_alive()):

        # say to arduino to drop a kit:
        try:
            arduino_supply.write(str.encode(DROP_KIT_IDENTIFIER))
        except:  # SerialTimeoutException (raised if communication timeout is reached)
            inoperative_arduino_actions("supply", "SerialTimeoutException al decir al arduino que puede dejar caer un kit") 

        # NOTE: The communication timeout of the arduino supply is much bigger than the arduino storage because it needs some seconds to drop a kit. 
        
        # receive from arduino the message that the kit has been dropped:
        kit_dropped = arduino_supply.read(DROP_KIT_RESPONSE_LENGTH).decode('UTF-8')
        if (len(kit_dropped) != DROP_KIT_RESPONSE_LENGTH):  # this will be the case of communication timeout reached (0 bytes read)
            inoperative_arduino_actions("storage", "Timeout de la comunicación con el arduino: no ha llegado a comunicar nada de vuelta a la Rpi")
            return False
        elif kit_dropped == DROP_KIT_FINISHED_FAILURE:
            inoperative_arduino_actions("storage", "Ha saltado el timeout del motor, eso significa que o el kit ha caído pero el sensor no ha sido capaz de detectarlo (y por tanto está roto) o ha ocurrido un problema con el motor o el tornillo sin fin o los kits se han encallado")
            return False
        elif kit_dropped == DROP_KIT_FINISHED_SUCCESS:
            return True
        else:
            print("Función drop_kit() de Arduino_controller: ha llegado a un estado no esperado. Arduino ha retornado: " + str(kit_dropped))
            return False

    else:
        inoperative_arduino_actions("supply", "No se detecta el arduino conectado")
        return False