from screeninfo import get_monitors #to check width and height of the monitor

# ------------ paths and constants -----------------------------

PROGRAM_SOURCE_CODE_PATH = "/home/ismael/Documentos/TFG/SALIBANK_PROGRAM/src"  # path of this file's directory. #TODO: En la rpi es /home/pi/Desktop/SALIBANK_PROGRAM/src

MACHINE_ID = "AAAA"  # each character can be a letter or a number. This means that each machine_ID has 36^4 = 1,679,616 different values. The Machine_ID is unique en each machine of SALIBANK, so it will printed with the current time in the users labels and it will be printed with the container number in the operators/admins labels when collecting samples 

PRINTER_PORT = "/dev/usb/lp5" # TODO: Cambiar al probarlo en Rpi. En la Rpi es /dev/usb/lp0
ARDUINO_STORAGE_PORT = "/dev/ttyACM1" # TODO: En la Rpi hay que ver qué path es
ARDUINO_SUPPLY_PORT = "/dev/ttyACM0" 

DB_MEDICALINFO_PATH = "../res/database/muestras_saliva.db" 
DB_USEINFO_PATH = "../res/database/info_uso.db"
IMAGES_DIRECTORY = "../res/images/"
ADMINSID_PATH = "../res/adminsAndOperators/admins.csv"
OPERATORSID_PATH = "../res/adminsAndOperators/operators.csv"
OPERATORS_EMAILS_PATH = "../res/adminsAndOperators/emails.csv"  # contains the operators emails to contact then in case of any problem
AVAILABLE_RESOURCES_AND_INFO_PATH = "../res/resources_&_info_data.csv"
SPANISH_LANGUAGE_PATH = "../res/languages/spanish.csv"
CATALAN_LANGUAGE_PATH = "../res/languages/catalan.csv"
ENGLISH_LANGUAGE_PATH = "../res/languages/english.csv"

STORED_SAMPLES_LIMIT = 50    
AVAILABLE_KITS_AFTER_REFILL = 20    
NUMBER_OF_LABELS_IN_LABEL_ROLL = 200     

SCREEN_WIDTH = 800#get_monitors()[0].width  # TODO: Cambiar en la Rpi por la funcion comentada
SCREEN_HEIGHT = 480#get_monitors()[0].height  # TODO: Cambiar en la Rpi por la funcion comentada

SALIBANK_MAIN_EMAIL = "salibanktfg@gmail.com"

SCREEN_SAVER_BACK_TIMER = 15000 # in miliseconds
INACTIVITY_CHECK_RESOURCES_TIMER = 1800000 # 30 min = 1800 seconds = 1800000 ms
CHECK_TEMPERATURE_TIMER = 20000 # in miliseconds 
LABEL_PRINTING_TIMEOUT = 3 # in seconds
INTERNET_CONNECTION_TIMEOUT = 2 # in seconds
ARDUINO_STORAGE_COMMUNICATION_TIMEOUT = 2 # in seconds
ARDUINO_SUPPLY_COMMUNICATION_TIMEOUT = 12 # in seconds

MIN_ALLOWED_TEMPERATURE = 0.0 # in centigrades. 
MAX_ALLOWED_TEMPERATURE = 40.0 # in centigrades. 

WARNING_STOCK_THRESHOLD = 0.4 # 40% 
ALARM_STOCK_THRESHOLD = 0.15 # 15%


CORRECT_PASSWORD_ENCRIPTED = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"  # The password for admins/operators is "1234" and this hash is the encription of "1234" with sha256. Remember to delete this comment in the final version of SALIBANK (this is prototype) because in this comment is shown the password decripted 



# ----- STYLE ------
CATSALUT_COLOR = "#7BACFC"
LIGHT_RED_BACKGROUNDCOLOR = "#ffa6a6"

ALARM_BACKGROUNDCOLOR = "#ffa6a6"
WARNING_BACKGROUNDCOLOR = "#ffeba6"
SAFE_BACKGROUNDCOLOR = "#a6ffa6"

CATSALUT_TEXT_FONT = "Helvetica Neue"
SCREEN_TITLE_TEXT_SIZE = 24
SCREEN_SECOND_TITLE_TEXT_SIZE = 20
SCREEN_THIRD_TITLE_TEXT_SIZE = 14
BUTTON_TEXT_SIZE = 16
SECONDARY_BUTTON_TEXT_SIZE = 14  # For not so relevant buttons in the application (like the change language button at login screen).
PARAGRAPH_TEXT_SIZE = 12
CONTROL_INFORMATION_TEXT_SIZE = 10  # For the control text boxes (only visible for admins and operators) indicating how much printer labels, kits and samples are in the system
APP_NOT_AVAILABLE_ERROR_TEXT_SIZE = 56