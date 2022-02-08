from screeninfo import get_monitors #to check width and height of the monitor

# ------------ paths and constants -----------------------------

PROGRAM_SOURCE_CODE_PATH = "/home/ismael/Documentos/TFG/SALIBANK_PROGRAM/src"  # path of this file's directory
# TODO IMPORTANTE: CAMBIAR LA LINEA DE ARRIBA CON EL PATH BUENO: /home/pi/Desktop/SALIBANK_PROGRAM/src !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

ARD1_PORT = "/dev/ttyUSB0"
ARD2_PORT = "/dev/ttyUSB1"
PRINTER_PORT = "/dev/usb/lp0"

DB_MEDICALINFO_PATH = "../res/database/muestras_saliva.db" 
DB_USEINFO_PATH = "../res/database/info_uso.db"
IMAGES_DIRECTORY = "../res/images/"
ADMINSID_PATH = "../res/adminsAndOperators/admins.csv"
OPERATORSID_PATH = "../res/adminsAndOperators/operators.csv"

STORED_SAMPLES_LIMIT = 50    # TODO: ponerlo a la cantidad maxima de muestras que se pueden poner
AVAILABLE_KITS_AFTER_REFILL = 20    # TODO: ponerlo a la cantidad de kits disponibles que vayan a caber en la maquina
NUMBER_OF_LABELS_IN_LABEL_ROLL = 200     # TODO: ponerlo a la cantidad de etiquetas que vengan en un rollo nuevo de la impresora

SCREEN_WIDTH = get_monitors()[0].width
SCREEN_HEIGHT = get_monitors()[0].height

SCREEN_SAVER_BACK_TIMER = 10000 # in miliseconds

WARNING_STOCK_THRESHOLD = 0.4 # 40% 
ALARM_STOCK_THRESHOLD = 0.15 # 15%

PREVIOUS_INFO_SALIVA_TEST = """Deben transcurrir un mínimo de 30 minutos entre la última vez que ingirió cualquier tipo de comida o líquido y la recogida de saliva. 

Si ha transcurrido ese tiempo, pulse el botón de "Cumplo los requisitos. Quiero recoger el kit".

Si NO ha transcurrido ese tiempo, retorne al menú anterior y cierre sesión. Vuelva más tarde."""


CORRECT_PASSWORD = "1234" # TODO: ESTO NO LO PODEMOS TENER ASÍ DE INSEGURO. 



# ----- STYLE ------
CATSALUT_COLOR = "#7BACFC"
#CATSALUT_COLOR2 = "#7db3e1"  I finally dont use it
#CATSALUT_COLOR3 = "#9fd2ec"  I finally dont use it
#LIGHT_GRAY_BACKGROUNDCOLOR = "#c0c0c0"  I finally dont use it
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