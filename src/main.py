from tkinter import *

import os

import constants
import Counters  # counters need to be imported before checker (because checker class imports counter class and counter class imports Priority from Checker class, so importing Checkers before Counters generates circular dependency). Also, all the classes that import Checker class need to be imported after this line (example: BDcontroller class imports ArduinoController class and ArduinoController class imports Checker, this is why BDcontroller is imported after than Counters here)
import DBcontroller
from Screen_saver import *
import Checker
import Language_controller
from Language_controller import Language
import Arduino_controller





os.chdir( constants.PROGRAM_SOURCE_CODE_PATH ) # Needed for relative paths to work in case that the program is launched from another location 
                                            # than the directory of this program. This must be the first line of this code.


DBcontroller.create_DBs_if_not_exist()
DBcontroller.init_admins_and_operators_info()
DBcontroller.add_new_event("-", "APLICACIÓN ENCENDIDA")

Counters.initialize_information()

root = Screen_manager.start_application()

# TODO: Descomentar linea para la rpi (al testear en PC tambien puedo descomentarla pero tendre que cambiar la contraseña)
#os.system("echo 'salibank' | sudo -S chmod 666 " + constants.PRINTER_PORT)  # R+W premission to the printer

Checker.check_hardware_usable_and_internet_connection_at_turningON() 
Checker.check_available_labels_at_turningON()
Checker.check_available_kits_at_turningON()
Checker.check_not_max_stored_samples_at_turningON()

Language_controller.set_current_language(Language.SPANISH)

Arduino_controller.init_arduinos_connections()
root.after(10000, Arduino_controller.get_deposit_temperature_periodically_and_update_DB) # 10 seconds after powering on: check temperature and update DB if needed. After that, a periodic interruption is programmed every X minutes to get the temperature again and repeat the process. 

Screen_saver.getInstance().go_to_screen_saver()

# TODO: Descomentar linea para la rpi
#root.attributes("-fullscreen", True)

mainloop()

