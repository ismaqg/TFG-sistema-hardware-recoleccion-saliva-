from tkinter import messagebox

import os.path

import smtplib
from email.message import EmailMessage

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

def is_arduino_supply_alive():
    #return True  # TODO: CAMBIAR ESTA LINEA POR EL CODIGO DE DEBAJO
    return os.path.exists(constants.ARDUINO_SUPPLY_PORT)

def is_arduino_storage_alive():
    #return True  # TODO: CAMBIAR ESTA LINEA POR EL CODIGO DE DEBAJO
    return os.path.exists(constants.ARDUINO_STORAGE_PORT)


def is_printer_alive():
    return True  # TODO: CAMBIAR ESTA LINEA POR EL CODIGO DE DEBAJO
    return os.path.exists(constants.PRINTER_PORT)
    
    



def notify_operator(problem_description, priority):
    receiver_email = DBcontroller.get_operators_emails()

    msg = EmailMessage()
    msg['Subject'] = "[" + priority.name + "]"
    msg['From'] = constants.SALIBANK_MAIN_EMAIL
    msg['To'] = ', '.join(receiver_email)
    msg.set_content(problem_description)

    server = smtplib.SMTP('localhost')
    server.send_message(msg)
    server.quit()



#ONLY CALLABLE  WHEN TURNING ON THE RASPBERRY (and the program)
def check_hardware_usable_at_turningON():
    # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
    problems = ''
    if not is_printer_alive():
        problems += 'PRINTER IS NOT CONNECTED OR NOT POWERED ON OR NOT WORKING\n'
    if not is_arduino_supply_alive():
        problems += 'ARDUINO SUPPLY MODULE IS NOT CONNECTED OR NOT WORKING\n'
    if not is_arduino_storage_alive():
        problems += 'ARDUINO STORAGE MODULE IS NOT CONNECTED OR NOT WORKING\n'    
    if problems != '':
        messagebox.showerror("PROBLEMAS CON EL HARDWARE", "La aplicación no puede iniciarse. Problemas con el hardware: " + problems)
        Screen_manager.get_root().destroy()
        raise Exception("THE PROGRAM CAN'T START BECAUSE:\n" + problems)

#ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_available_labels_at_turningON():
    # TODO: Test function!! 
    if Counters.get_available_labels() == 0: # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
        messagebox.showerror(Language_controller.get_message("necesaria reposicion etiquetas (cabecera)"), Language_controller.get_message("necesaria reposicion etiquetas (cuerpo)")) # NOTE: This function is blocking until OK is pressed (and when OK is pressed it's supposed that the operator has refilled labels)
        # double checking because the operator who is turning on the machine maybe doesn't have available labels so the machine needs to shut down instead of saving the information of "labels refilled":
        if Counters.get_available_labels() == 0:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITHOUT LABELS ON THE PRINTER")
        else:
            Counters.set_available_labels(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN REPLENISHED LABELS AT POWER UP")

#ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_available_kits_at_turningON():
    # TODO: Test function!! 
    if Counters.get_available_kits() == 0: # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
        messagebox.showerror(Language_controller.get_message("necesaria reposicion kits (cabecera)"), Language_controller.get_message("necesaria reposicion kits (cuerpo)"))  # NOTE: This function is blocking until OK is pressed (and when OK is pressed it's supposed that the operator has refilled kits)
        # double checking because the operator who is turning on the machine maybe doesn't have available kits so the machine needs to shut down instead of saving the information of "kits refilled":
        if Counters.get_available_kits() == 0:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITHOUT AVAILABLE KITS")
        else:
            Counters.set_available_kits(constants.AVAILABLE_KITS_AFTER_REFILL)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN REPLENISHED KITS AT POWER UP")

# ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_not_max_stored_samples_at_turningON():
    if Counters.get_stored_samples() == constants.STORED_SAMPLES_LIMIT:
        # TODO: Testear esto. O sea, testear que en un turningON funcione bien todo lo que tiene que ocurrir acerca de recoger muestras.
        messagebox.showerror(Language_controller.get_message("necesario vaciado deposito muestras (cabecera)"), Language_controller.get_message("necesario vaciado deposito muestras (cuerpo)"))
        MainScreen._collect_samples()

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



