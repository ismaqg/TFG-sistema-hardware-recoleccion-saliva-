import constants
import Checker
from Checker import Priority
import DBcontroller
import Screen_manager



__available_kits = None 
__stored_samples = None 
__available_labels = None

def initialize_information():
    global __available_kits, __stored_samples, __available_labels
    __available_kits, __stored_samples, __available_labels = DBcontroller.read_available_resources_csv()
    

def get_available_kits():
    global __available_kits
    return __available_kits

def get_stored_samples():
    global __stored_samples
    return __stored_samples

def get_available_labels():
    global __available_labels
    return __available_labels



def set_available_kits(x):
    global __available_kits
    __available_kits = x
    DBcontroller.write_available_resources_csv(__available_kits, __stored_samples, __available_labels)

def set_stored_samples(x):
    global __stored_samples
    __stored_samples = x
    DBcontroller.write_available_resources_csv(__available_kits, __stored_samples, __available_labels)

def set_available_labels(x):
    global __available_labels
    __available_labels = x
    DBcontroller.write_available_resources_csv(__available_kits, __stored_samples, __available_labels)



def decrement_available_kits():
    global __available_kits
    if __available_kits == 0:
        Screen_manager.get_root().destroy()
        raise Exception ("trying to decrement available kits when there are 0 available kits")
    if __available_kits == 1:
        Checker.notify_operator("Se han acabado los kits", Priority.CRITICAL)
        DBcontroller.add_new_event("-", "SE HAN ACABDO KITS")
    elif float(__available_kits) > constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL  and  float(__available_kits-1) <= int(constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):  # the decrease in kits has made us just reach the alarm threshold
        Checker.notify_operator("Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de los kits", Priority.HIGH)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de los kits")
    elif float(__available_kits) > int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL)  and  float(__available_kits-1) <= int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):  # the decrease in kits has made us just reach the warning threshold
        Checker.notify_operator("Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de los kits", Priority.MEDIUM)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de los kits")
    __available_kits -= 1
    DBcontroller.write_available_resources_csv(__available_kits, __stored_samples, __available_labels)
    

def increment_stored_samples():
    global __stored_samples
    if __stored_samples == constants.STORED_SAMPLES_LIMIT:
        Screen_manager.get_root().destroy()
        raise Exception ("trying to increment stored samples when there is no empty space")
    if __stored_samples == constants.STORED_SAMPLES_LIMIT - 1:
        Checker.notify_operator("No queda espacio para muestras", Priority.CRITICAL)
        DBcontroller.add_new_event("-", "NO QUEDA ESPACIO PARA MUESTRAS")
    elif float(__stored_samples) < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT)  and  float(__stored_samples-1) >= int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):  # the increase in storedsamples has made us just reach the alarm threshold
        Checker.notify_operator("Se ha llenado más del del " + (1-constants.ALARM_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva", Priority.HIGH)
        DBcontroller.add_new_event("-", "Se ha llenado más del del " + (1-constants.ALARM_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva")
    elif float(__stored_samples) < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT)  and  float(__stored_samples-1) >= int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):  # the increase in storedsamples has made us just reach the warning threshold
        Checker.notify_operator("Se ha llenado más del del " + (1-constants.WARNING_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva", Priority.MEDIUM)
        DBcontroller.add_new_event("-", "Se ha llenado más del del " + (1-constants.WARNING_STOCK_THRESHOLD)*100 + " del espacio para muestras de saliva")
    __stored_samples += 1
    DBcontroller.write_available_resources_csv(__available_kits, __stored_samples, __available_labels)


def decrement_available_labels():
    global __available_labels
    if __available_labels == 0:
        Screen_manager.get_root().destroy()
        raise Exception ("trying to decrement available labels when there are 0 available labels")
    if __available_labels == 1:
        Checker.notify_operator("Se han acabado las etiquetas", Priority.CRITICAL)
        DBcontroller.add_new_event("-", "SE HAN ACABADO LAS ETIQUETAS")
    elif float(__available_labels) > constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL  and  float(__available_labels-1) <= int(constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):  # the decrease in labels has made us just reach the alarm threshold
        Checker.notify_operator("Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de las etiquetas", Priority.HIGH)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.ALARM_STOCK_THRESHOLD*100 + " porciento de las etiquetas")
    elif float(__available_labels) > int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL)  and  float(__available_labels-1) <= int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):  # the decrease in labels has made us just reach the warning threshold
        Checker.notify_operator("Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de las etiquetas", Priority.MEDIUM)
        DBcontroller.add_new_event("-", "Queda menos del " + constants.WARNING_STOCK_THRESHOLD*100 + " porciento de las etiquetas")
    __available_labels -= 1
    DBcontroller.write_available_resources_csv(__available_kits, __stored_samples, __available_labels)



def get_available_labels_fg_color():
    global __available_labels
    if __available_labels > int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return "green"
    elif __available_labels > int(constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return "#ffae00"
    else:
        return "red"

def get_available_labels_bg_color():
    global __available_labels
    if __available_labels > int(constants.WARNING_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return constants.SAFE_BACKGROUNDCOLOR
    elif __available_labels > int(constants.ALARM_STOCK_THRESHOLD * constants.NUMBER_OF_LABELS_IN_LABEL_ROLL):
        return constants.WARNING_BACKGROUNDCOLOR
    else:
        return constants.ALARM_BACKGROUNDCOLOR

def get_available_kits_fg_color():
    global __available_kits
    if __available_kits > int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return "green"
    elif __available_kits > int(constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return "#ffae00"
    else:
        return "red"

def get_available_kits_bg_color():
    global __available_kits
    if __available_kits > int(constants.WARNING_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return constants.SAFE_BACKGROUNDCOLOR
    elif __available_kits > int(constants.ALARM_STOCK_THRESHOLD * constants.AVAILABLE_KITS_AFTER_REFILL):
        return constants.WARNING_BACKGROUNDCOLOR
    else:
        return constants.ALARM_BACKGROUNDCOLOR

def get_stored_samples_fg_color():
    global __stored_samples
    if __stored_samples < int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return "green"
    elif __stored_samples < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return "#ffae00"
    else:
        return "red"

def get_stored_samples_bg_color():
    global __stored_samples
    if __stored_samples < int((1 - constants.WARNING_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return constants.SAFE_BACKGROUNDCOLOR
    elif __stored_samples < int((1 - constants.ALARM_STOCK_THRESHOLD) * constants.STORED_SAMPLES_LIMIT):
        return constants.WARNING_BACKGROUNDCOLOR
    else:
        return constants.ALARM_BACKGROUNDCOLOR