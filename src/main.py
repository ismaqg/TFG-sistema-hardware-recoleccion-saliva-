from tkinter import *

import os
import constants
import DBcontroller
from Screen_saver import *




# ------------ path of this file's directory -------------------
os.chdir( constants.PROGRAM_DIRECTORY_PATH ) # Needed for relative paths to work in case that the program is launched from another location 
                                            # than the directory of this program. This must be the first line of this code.



# ------------------- global variables ---------------------------
# counters:
available_kits = constants.AVAILABLE_KITS_AFTER_REFILL 
stored_samples = 0 
available_labels = constants.NUMBER_OF_LABELS_IN_LABEL_ROLL 

# operators and admins IDs:
admins = DBcontroller.get_admins()
operators = DBcontroller.get_operators()


# -------- tkinter variables ----------------


# --------- Graphic App Creation ------------
root = Screen_manager.start_application()



# --------- Main application code ----------- 
DBcontroller.create_DB_if_not_exists()

screen_saver_screen = Screen_saver()



# -------- Looping the application ----------
root.mainloop()

