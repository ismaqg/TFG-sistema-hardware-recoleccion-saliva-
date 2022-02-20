from tkinter import messagebox

import Checker
import DBcontroller
from Not_available import Not_available
from Person import ActivePerson
import Language_controller


def inoperative_arduino_actions():
    Checker.notify_operator("ARDUINO INOPERATIVO", Checker.Priority.CRITICAL)
    DBcontroller.add_new_event("-", "APP CLOSED. ARDUINO INOPERATIVE")
    messagebox.showerror(Language_controller.get_message("error recogida kit (cabecera)"), Language_controller.get_message("error recogida kit (cuerpo)"))  
    ActivePerson.getCurrent().logOut()
    Not_available.getInstance().go_to_not_available_screen()