import constants

available_kits = constants.AVAILABLE_KITS_AFTER_REFILL 
stored_samples = 0 
available_labels = constants.NUMBER_OF_LABELS_IN_LABEL_ROLL

def initialize_information():
    # TODO: ESOS VALORES HARDCODEADOS ESTAN PARA TESTING, PERO EN LA VERSION DEFINITIVA DEBO CAMBIAR ESOS VALORES POR LO COMENTADO A LA DERECHA
    global available_kits, stored_samples, available_labels
    available_kits = 5  #constants.AVAILABLE_KITS_AFTER_REFILL 
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
    available_kits -= 1

def increment_stored_samples():
    global stored_samples
    stored_samples += 1

def decrement_available_labels():
    global available_labels
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