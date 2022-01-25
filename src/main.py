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



# -------- tkinter variables ----------------


# --------- Main application code ----------- 
root = Screen_manager.start_application()

DBcontroller.create_DBs_if_not_exist()
DBcontroller.init_admins_and_operators_info()

Screen_saver.getInstance().go_to_screen_saver()



# -------- Looping the application ----------
root.attributes("-fullscreen", True)
root.mainloop()

