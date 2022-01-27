from tkinter import *

import os
import constants
import DBcontroller
import Counters
from Screen_saver import *




# ------------ path of this file's directory -------------------
os.chdir( constants.PROGRAM_DIRECTORY_PATH ) # Needed for relative paths to work in case that the program is launched from another location 
                                            # than the directory of this program. This must be the first line of this code.




# --------- Main application code ----------- 
DBcontroller.create_DBs_if_not_exist()
DBcontroller.init_admins_and_operators_info()
DBcontroller.add_new_event("-", "APLICACIÓN ENCENDIDA")

Counters.initialize_information()

root = Screen_manager.start_application()
Screen_saver.getInstance().go_to_screen_saver()



# -------- Looping the application ----------
root.attributes("-fullscreen", True)
mainloop() # TODO: Probar a poner root.mainloop a ver si se fastidia algo en lo del nuevo toplevel para la admin authentication

