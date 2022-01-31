import constants
from Checker import Priority
import Checker
import DBcontroller

available_kits = constants.AVAILABLE_KITS_AFTER_REFILL 
stored_samples = 0 
available_labels = constants.NUMBER_OF_LABELS_IN_LABEL_ROLL

def initialize_information():
    # TODO: ESOS VALORES HARDCODEADOS ESTAN PARA TESTING, PERO EN LA VERSION DEFINITIVA DEBO CAMBIAR ESOS VALORES POR LO COMENTADO A LA DERECHA DEL TODO
    global available_kits, stored_samples, available_labels
    available_kits = 0 #5  #constants.AVAILABLE_KITS_AFTER_REFILL 
    stored_samples = 47  #0 
    available_labels = 72  #constants.NUMBER_OF_LABELS_IN_LABEL_ROLL



def get_available_kits():
    global available_kits
    return available_kits

def get_stored_samples():
    global stored_samples
    return stored_samples

def get_available_labels():
    global available_labels
    return available_labels



def set_available_kits(x):
    global available_kits
    available_kits = x

def set_stored_samples(x):
    global stored_samples
    stored_samples = x

def set_available_labels(x):
    global available_labels
    available_labels = x



def decrement_available_kits():
    global available_kits
    if available_kits == 0:
        raise Exception ("trying to decrement available kits when there are 0 available kits")
    if available_kits == 1:
        Checker.notify_operator("Se han acabado los kits", Priority.CRITICAL)
        DBcontroller.add_new_event("-", "SE HAN ACABDO KITS")
    elif float(available_kits) > constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL  and  float(available_kits-1) <= int(constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):  # the decrease in kits has made us just reach the alarm threshold
        Checker.notify_operator("Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de los kits", Priority.HIGH)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de los kits")
    elif float(available_kits) > int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL)  and  float(available_kits-1) <= int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):  # the decrease in kits has made us just reach the warning threshold
        Checker.notify_operator("Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de los kits", Priority.MEDIUM)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de los kits")
    available_kits -= 1
    

def increment_stored_samples():
    global stored_samples
    if stored_samples == constants.STORED_SAMPLES_LIMIT:
        raise Exception ("trying to increment stored samples when there is no empty space")
    if available_kits == constants.STORED_SAMPLES_LIMIT - 1:
        Checker.notify_operator("No queda espacio para muestras", Priority.CRITICAL)
        DBcontroller.add_new_event("-", "NO QUEDA ESPACIO PARA MUESTRAS")
    elif float(stored_samples) < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT)  and  float(stored_samples-1) >= int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):  # the increase in storedsamples has made us just reach the alarm threshold
        Checker.notify_operator("Se ha llenado más del del " + (1-constants.ALARM_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva", Priority.HIGH)
        DBcontroller.add_new_event("-", "Se ha llenado más del del " + (1-constants.ALARM_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva")
    elif float(stored_samples) < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT)  and  float(stored_samples-1) >= int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):  # the increase in storedsamples has made us just reach the warning threshold
        Checker.notify_operator("Se ha llenado más del del " + (1-constants.WARNING_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva", Priority.MEDIUM)
        DBcontroller.add_new_event("-", "Se ha llenado más del del " + (1-constants.WARNING_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva")
    stored_samples += 1


def decrement_available_labels():
    global available_labels
    if available_labels == 0:
        raise Exception ("trying to decrement available labels when there are 0 available labels")
    if available_labels == 1:
        Checker.notify_operator("Se han acabado las etiquetas", Priority.CRITICAL)
        DBcontroller.add_new_event("-", "SE HAN ACABADO LAS ETIQUETAS")
    elif float(available_labels) > constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL  and  float(available_labels-1) <= int(constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):  # the decrease in labels has made us just reach the alarm threshold
        Checker.notify_operator("Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de las etiquetas", Priority.HIGH)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de las etiquetas")
    elif float(available_labels) > int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL)  and  float(available_labels-1) <= int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):  # the decrease in labels has made us just reach the warning threshold
        Checker.notify_operator("Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de las etiquetas", Priority.MEDIUM)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de las etiquetas")
    available_labels -= 1



def get_available_labels_fg_color():
    global available_labels
    if available_labels > int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return "green"
    elif available_labels > int(constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return "#ffae00"
    else:
        return "red"

def get_available_labels_bg_color():
    global available_labels
    if available_labels > int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return constants.SAFE_BACKGROUNDCOLOR
    elif available_labels > int(constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return constants.WARNING_BACKGROUNDCOLOR
    else:
        return constants.ALARM_BACKGROUNDCOLOR

def get_available_kits_fg_color():
    global available_kits
    if available_kits > int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return "green"
    elif available_kits > int(constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return "#ffae00"
    else:
        return "red"

def get_available_kits_bg_color():
    global available_kits
    if available_kits > int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return constants.SAFE_BACKGROUNDCOLOR
    elif available_kits > int(constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return constants.WARNING_BACKGROUNDCOLOR
    else:
        return constants.ALARM_BACKGROUNDCOLOR

def get_stored_samples_fg_color():
    global stored_samples
    if stored_samples < int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return "green"
    elif stored_samples < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return "#ffae00"
    else:
        return "red"

def get_stored_samples_bg_color():
    global stored_samples
    if stored_samples < int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return constants.SAFE_BACKGROUNDCOLOR
    elif stored_samples < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return constants.WARNING_BACKGROUNDCOLOR
    else:
        return constants.ALARM_BACKGROUNDCOLOR