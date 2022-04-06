from tkinter import messagebox

import Checker
import DBcontroller
from Not_available_screen import Not_available_screen
from Person import ActivePerson
import Language_controller


def inoperative_arduino_actions():
    Checker.notify_operator("ARDUINO INOPERATIVO", Checker.Priority.CRITICAL)
    DBcontroller.add_new_event("-", "APP CLOSED. ARDUINO INOPERATIVE")
    messagebox.showerror(Language_controller.get_message("error recogida kit (cabecera)"), Language_controller.get_message("error recogida kit (cuerpo)"))  
    ActivePerson.getCurrent().logOut()
    Not_available_screen.getInstance().go_to_Not_available_screen_screen()

def get_deposit_temperature():
    #TODO. Y lee lo de abajo que tambien aplica a esta funcion
    return "99.9"

""" IMPORTANTE: LEE ESTE TODO DE ABAJO """
# TODO: Creo que sería mejor que se pudiesen llamar tal cual a las funciones de Arduino_controller y que se hiciese allí dentro toda la gestión que hay que hacer si arduino está inoperativo. O sea, que sea dentro de esta clase donde se llame a Checker.is_arduino_alive(), la gestión de timeouts y el salto a NotAvailableScreen