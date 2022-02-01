from tkinter import messagebox

import os.path

import Counters
import constants
import DBcontroller
import Screen_manager
from Person import ActivePerson
from enum import Enum


#ENUM:
Priority = Enum("Priority", "CRITICAL HIGH MEDIUM LOW")

def is_arduino_alive():
    # TODO. Mirar si esta vivo (y retornar true o false en consecuencia). En caso de no estar vivo hay que avisar del problema critico: notify_operator("ARDUINO NOT RESPONDING", Priority.CRITICAL)
    return True

def is_printer_alive():
    return True  # TODO: CAMBIAR ESTA LINEA POR EL CODIGO DE DEBAJO
    """
    return os.path.exists(constants.PRINTER_PORT)
    """
    



def notify_operator(problem_description, priority):
    # TODO: ENVIAR CORREO OPERADOR CON EL PROBLEMA CRITICO. Lo de prioridad es para saber como de alarmante poner el asunto del correo 
    pass



#ONLY CALLABLE  WHEN TURNING ON THE RASPBERRY (and the program)
def check_hardware_usable_at_turningON():
    # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
    problems = ''
    if not is_printer_alive():
        problems += 'PRINTER IS NOT CONNECTED OR NOT POWERED ON OR NOT WORKING\n'
    if not is_arduino_alive():
        problems += 'ARDUINO IS NOT CONNECTED OR NOT WORKING\n'    
    if problems != '':
        Screen_manager.get_root().destroy()
        raise Exception("THE PROGRAM CAN'T START BECAUSE:\n. PLEASE CHECK THAT THEY ARE WELL CONNECTED AND TURNED ON / WORKING" + problems)

#ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_available_labels_at_turningON():
    # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
    if Counters.get_available_labels() == 0:
        messagebox.showerror("ERROR. NO HAY ETIQUETAS", "El programa no puede iniciarse porque no quedan etiquetas en la impresora. Por favor, introduce un nuevo rollo en ella. Haz click en OK cuando lo hayas hecho")
        response = messagebox.askyesno("REPOSICIÓN DE ETIQUETAS", "Estas seguro de haber introducido un nuevo rollo de etiquetas?")
        if response == False:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITHOUT LABELS ON THE PRINTER")
        else:
            Counters.set_available_labels(constants.NUMBER_OF_LABELS_IN_LABEL_ROLL)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN REPUSO ETIQUETAS EN EL ENCENDIDO, PARA HACER OPERABLE LA MÁQUINA")

#ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_available_kits_at_turningON():
    # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
    if Counters.get_available_kits() == 0:
        messagebox.showerror("ERROR. NO HAY KITS", "El programa no puede iniciarse porque no queda ningún kit que puedan utilizar los usuarios. Por favor, rellena el depósito de kits. Haz click en OK cuando lo hayas hecho")
        response = messagebox.askyesno("REPOSICIÓN DE KITS", "Estas seguro de haber rellenado completamente el depósito de kits disponibles?")
        if response == False:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITHOUT AVAILABLE KITS")
        else:
            Counters.set_available_kits(constants.AVAILABLE_KITS_AFTER_REFILL)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN REPUSO KITS EN EL ENCENDIDO, PARA HACER OPERABLE LA MÁQUINA")

# ONLY CALLABLE WHEN TURNING ON THE RASPBERRY (and the program)
def check_not_max_stored_samples_at_turningON():
    # NOTE: Here we do not send a message to the operator because it is assumed that the machine has been turned on by an operator / admin
    if Counters.get_stored_samples() == constants.STORED_SAMPLES_LIMIT:
        messagebox.showerror("ERROR. DEPOSITO LLENO", "El programa no puede iniciarse porque el depósito de muestras está lleno y necesita vaciarse. Por favor, vacía el depósito de muestras. Haz click en OK cuando lo hayas hecho")
        response = messagebox.askyesno("REPOSICIÓN DE KITS", "Estas seguro de haber vaciado completamente el depósito de muestras?")
        if response == False:
            Screen_manager.get_root().destroy()
            raise Exception("PROGRAM CAN'T START WITH FULL SALIVA SAMPLE CONTAINER")
        else:
            Counters.set_stored_samples(0)
            DBcontroller.add_new_event("-", "OPERADOR/ADMIN VACIÓ DEPÓSITO MUESTRAS EN EL ENCENDIDO, PARA HACER OPERABLE LA MÁQUINA")


def check_available_resources_at_user_logIn():
    problems = ''
    if Counters.get_stored_samples() == constants.STORED_SAMPLES_LIMIT:
        problems += 'El deposito de muestras está lleno.\n'
    if Counters.get_available_kits() == 0:
        problems += 'No quedan kits.\n'
    if Counters.get_available_labels() == 0:
        problems += 'No quedan etiquetas.\n'
    if not is_arduino_alive():
        problems += 'Arduino inoperativo.\n'
    if not is_printer_alive():
        problems += 'Impresora inoperativa.\n'

    if problems == '':
        return True
    else:  # if this occurs, a message is displayed, the event is registered and the rpi is powered off
        print("Los problemas internos son: " + problems) 
        DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "USER LOGIN FAIL. NO AVAILABLE RESOURCES:\n" + problems)
        notify_operator("Un usuario no he podido hacer login por los siguientes problemas: \n" + problems + " Por ende, se ha apagado la máquina", Priority.CRITICAL)
        return False



