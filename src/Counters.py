import constants

available_kits = constants.AVAILABLE_KITS_AFTER_REFILL 
stored_samples = 0 
available_labels = constants.NUMBER_OF_LABELS_IN_LABEL_ROLL

def initialize_information():
    global available_kits, stored_samples, available_labels
    available_kits = constants.AVAILABLE_KITS_AFTER_REFILL 
    stored_samples = 0 
    available_labels = constants.NUMBER_OF_LABELS_IN_LABEL_ROLL



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
