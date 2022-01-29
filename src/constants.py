from screeninfo import get_monitors #to check width and height of the monitor

# ------------ paths and constants -----------------------------

PROGRAM_DIRECTORY_PATH = "/home/ismael/Documentos/TFG/CODIGO_ISMA/src"  # path of this file's directory
# TODO IMPORTANTE: CAMBIAR LA LINEA DE ARRIBA CON EL PATH BUENO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

CATSALUT_COLOR = "#7BACFC"
CATSALUT_COLOR2 = "#7db3e1"
CATSALUT_COLOR3 = "#9fd2ec"
LIGHT_GRAY_BACKGROUNDCOLOR = "#c0c0c0"
LIGHT_RED_BACKGROUNDCOLOR = "#ffa6a6"

ALARM_BACKGROUNDCOLOR = "#ffa6a6"
WARNING_BACKGROUNDCOLOR = "#ffeba6"
SAFE_BACKGROUNDCOLOR = "#a6ffa6"

WARNING_STOCK_THRESHOLD = 0.4 # 40% 
ALARM_STOCK_THRESHOLD = 0.15 # 15%

CORRECT_PASSWORD = "1234" # TODO: ESTO NO LO PODEMOS TENER ASÍ DE INSEGURO. 