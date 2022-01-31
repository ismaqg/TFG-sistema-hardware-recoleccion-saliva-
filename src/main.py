from tkinter import *

import os
import constants
import DBcontroller
import Counters
from Screen_saver import *
import Checker




# ------------ path of this file's directory -------------------
os.chdir( constants.PROGRAM_DIRECTORY_PATH ) # Needed for relative paths to work in case that the program is launched from another location 
                                            # than the directory of this program. This must be the first line of this code.




# --------- Main application code ----------- 
DBcontroller.create_DBs_if_not_exist()
DBcontroller.init_admins_and_operators_info()
DBcontroller.add_new_event("-", "APLICACIÓN ENCENDIDA")

Counters.initialize_information()

root = Screen_manager.start_application()

Checker.check_hardware_usable_at_turningON()
Checker.check_available_labels_at_turningON()
Checker.check_available_kits_at_turningON()
Checker.check_not_max_stored_samples_at_turningON()

Screen_saver.getInstance().go_to_screen_saver()



# -------- Looping the application ----------
root.attributes("-fullscreen", True)
mainloop() # TODO: Probar a poner root.mainloop a ver si se fastidia algo en lo del nuevo toplevel para la admin authentication

