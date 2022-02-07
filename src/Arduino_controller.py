from tkinter import messagebox

import Checker
import DBcontroller
from Not_available import Not_available
from Person import ActivePerson


def inoperative_arduino_actions():
    Checker.notify_operator("ARDUINO INOPERATIVO", Checker.Priority.CRITICAL)
    DBcontroller.add_new_event("-", "APP CLOSED. ARDUINO INOPERATIVE")
    messagebox.showerror("ERROR RECOGIDA KIT", "Lo sentimos, se ha producido un error interno. Se cerrará su sesión, vuelva más tarde por favor.")  
    ActivePerson.getCurrent().logOut()
    Not_available.getInstance().go_to_not_available_screen()