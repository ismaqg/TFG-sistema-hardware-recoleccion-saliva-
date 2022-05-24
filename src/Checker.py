from tkinter import messagebox

import os.path

import smtplib
from email.message import EmailMessage
import requests

import Counters
from MainScreen import MainScreen
import constants
import DBcontroller
import Screen_manager
import Language_controller
from Person import ActivePerson
from enum import Enum


#ENUM:
Priority = Enum("Priority", "CRITICAL HIGH MEDIUM LOW")

# TODO: Descomentar el "return true" de los siguientes 4 metodos para testeos donde vaya a faltar alguno de los componentes en cuestión
def is_arduino_supply_alive():
    #return True  
    return os.path.exists(constants.ARDUINO_SUPPLY_PORT)

def is_arduino_storage_alive():
    #return True  
    return os.path.exists(constants.ARDUINO_STORAGE_PORT)

def is_printer_alive():
    #return True  
    return os.path.exists(constants.PRINTER_PORT)
    
    
def is_internet_connection():
    # return True
    url = "https://www.google.com/"
    try:
        request = requests.get(url, timeout = constants.INTERNET_CONNECTION_TIMEOUT)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False



def notify_operator(problem_description, priority):
    receiver_email = DBcontroller.get_operators_emails()
    try:
        msg = EmailMessage()
        msg['Subject'] = "[" + priority.name + "]"
        msg['From'] = constants.SALIBANK_MAIN_EMAIL
        msg['To'] = ', '.join(receiver_email)
        msg.set_content(problem_description)

        server = smtplib.SMTP('localhost')
        server.send_message(msg)
        server.quit()
    except:
        if not is_internet_connection():
            # NOTE that in a definitive version this need to be changed to some way to communicate with the operator without internet.
            print("Not able to send email to Operators: No internet connection")  
        else:
            print("Not able to send email to Operators: There is internet connection but it couldn't send the email")
        

#ONLY CALLABLE  WHEN TURNING ON THE RASPBERRY (and the program)
def check_hardware_usable_and_internet_connection_at_turningON():
    # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
    problems = ''
    if not is_printer_alive():
        problems += 'PRINTER IS NOT CONNECTED OR NOT POWERED ON OR NOT WORKING\n'
    if not is_arduino_supply_alive():
        problems += 'ARDUINO SUPPLY MODULE IS NOT CONNECTED OR NOT WORKING\n'
    if not is_arduino_storage_alive():
        problems += 'ARDUINO STORAGE MODULE IS NOT CONNECTED OR NOT WORKING\n'
    if not is_internet_connection():
        problems += 'NO INTERNET CONNECTION\n'
    if problems != '':
        messagebox.showerror("PROBLEMAS EN EL INICIO", "La aplicación no puede iniciarse. Problemas hardware o de conexión detectados: " + problems)
        Screen_manager.get_root().destroy()
        raise Exception("THE PROGRAM CAN'T START BECAUSE:\n" + problems)

#ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_available_labels_at_turningON():
    if Counters.get_available_labels() == 0: # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
        messagebox.showerror(Language_controller.get_message("necesaria reposicion etiquetas (cabecera)"), Language_controller.get_message("necesaria reposicion etiquetas (cuerpo)")) 
        refilled = messagebox.askyesno(Language_controller.get_message("comprobacion reposicion etiquetas (cabecera)"), Language_controller.get_message("comprobacion reposicion etiquetas (cuerpo)"))
        if refilled:
            Counters.set_available_labels(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN REPLENISHED LABELS AT POWER UP")
        else:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITHOUT LABELS ON THE PRINTER")

#ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_available_kits_at_turningON(): 
    if Counters.get_available_kits() == 0: # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
        messagebox.showerror(Language_controller.get_message("necesaria reposicion kits (cabecera)"), Language_controller.get_message("necesaria reposicion kits (cuerpo)"))  
        refilled = messagebox.askyesno(Language_controller.get_message("comprobacion reposicion kits (cabecera)"), Language_controller.get_message("comprobacion reposicion kits (cuerpo)"))
        if refilled:
            Counters.set_available_kits(constants.AVAILABLE_KITS_AFTER_REFILL)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN REPLENISHED KITS AT POWER UP")
        else:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITHOUT AVAILABLE KITS")

# ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_not_max_stored_samples_at_turningON():
    if Counters.get_stored_samples() == constants.STORED_SAMPLES_LIMIT:
        messagebox.showerror(Language_controller.get_message("necesario vaciado deposito muestras (cabecera)"), Language_controller.get_message("necesario vaciado deposito muestras (cuerpo)"))
        MainScreen._collect_samples()  # an operator is always able to do this (doesn't need extra resources), this is why we don't show a message saying "were you able to empty the samples container?"

def check_available_resources():
    problems = ''
    if Counters.get_stored_samples() == constants.STORED_SAMPLES_LIMIT:
        problems += 'El deposito de muestras está lleno.\n'
    if Counters.get_available_kits() == 0:
        problems += 'No quedan kits.\n'
    if Counters.get_available_labels() == 0:
        problems += 'No quedan etiquetas.\n'
    if not is_arduino_supply_alive():
        problems += 'Arduino supply inoperativo.\n'
    if not is_arduino_storage_alive():
        problems += 'Arduino storage inoperativo.\n'
    if not is_printer_alive():
        problems += 'Impresora inoperativa.\n'
    if not is_internet_connection():
        problems += 'NO INTERNET CONNECTION\n'

    if problems == '':
        return True
    else:  # if this occurs, a message is displayed, the event is registered and the rpi is powered off
        print("Los problemas internos son: " + problems)
        if ActivePerson.isThereActivePerson():  # function called because someone tried to log in
            DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "USER LOGIN FAIL. NO AVAILABLE RESOURCES:\n" + problems)
        else:  # function called because it has been seen that all the resources do not work well after a period of inactivity of the machine
            DBcontroller.add_new_event("-", "AFTER INACTIVITY, DETECTED NO AVAILABLE RESOURCES:\n" + problems)
        notify_operator("SALIBANK es inoperable por los siguientes problemas críticos : \n" + problems, Priority.CRITICAL)
        return False



