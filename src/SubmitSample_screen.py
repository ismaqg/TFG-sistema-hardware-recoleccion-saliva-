from tkinter import *
from tkinter import messagebox

import Screen_manager
import constants

class SubmitSample_screen: # singleton
    
    __instance = None

    @staticmethod
    def getInstance():
        if SubmitSample_screen.__instance == None:
            SubmitSample_screen()
        return SubmitSample_screen.__instance

    def __init__(self):
        if SubmitSample_screen.__instance != None:
            raise Exception("SubmitSample_screen class is singleton")
        else:
            self.__current_step = 0

            self.__submitSampleScreen_frame = Screen_manager.init_screen_frame()
            self.__submitS_header_frame = Screen_manager.header_frame( self.__submitSampleScreen_frame)
            self.__submitS_body_frame = Screen_manager.body_frame( self.__submitSampleScreen_frame)

            self.__title = Label(self.__submitS_header_frame, text = "ENTREGAR MUESTRA", bg = constants.CATSALUT_COLOR, font = ("Verdana", 26, 'bold'))
            self.__return_b = Button(self.__submitS_header_frame, text = "VOLVER\nATRÁS", borderwidth=5, font = ("Verdana", 22, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__return_b.grid(row = 0, column = 1, sticky = 'NSEW', pady=20, padx=10)

            self.__submitS_header_frame.columnconfigure(0, weight=5)
            self.__submitS_header_frame.columnconfigure(1, weight=1)
            self.__submitS_header_frame.rowconfigure(0, weight=1)  # it's necessary to give a weight (even though there is only one row in clamKitscreen_header_frame) for sticky=NSEW of the inside widgets to work correctly


            self.__info_steps_title = Label(self.__submitS_body_frame, text = "PASO 1:", bg = "white", fg = constants.CATSALUT_COLOR, font = ("Verdana", 22, 'bold'))
            self.__info_steps_displayer = Canvas(self.__submitS_body_frame)
            self.__next_step_b = Button(self.__submitS_body_frame, text = "SIGUIENTE", borderwidth=3, font = ("Verdana", 22, 'bold'), command = self.__next_step)

            self.__info_steps_title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__info_steps_displayer.grid(row = 1, column = 0, sticky = 'NSEW', padx = 20)
            self.__next_step_b.grid(row = 2, column=0, sticky = 'NSEW', padx=120, pady = 5)

            self.__submitS_body_frame.rowconfigure(0, weight = 1)
            self.__submitS_body_frame.rowconfigure(1, weight = 8)
            self.__submitS_body_frame.rowconfigure(2, weight = 1)
            self.__submitS_body_frame.columnconfigure(0, weight = 1) # it's necessary to give a weight (even though there is only one column in clamKitscreen_body_frame) for sticky=NSEW of the inside widgets to work correctly
            

            SubmitSample_screen.__instance = self


    def __previous_screen(self):
        from MainScreen_user import MainScreen_user  # declared here to avoid circular dependency. It cannot be declared at the beggining of the file cannot be declared at the top of the file or in the constructor
        MainScreen_user.getInstance().go_to_main_screen()

    def __next_step(self):
        # TODO. 
        # nota: el boton de siguiente va cambiando de nombre a veces. (se puede convertir en imprimir etiqueta o en siguiente o tal)
        # nota: aqui puedo comprobar que la etiqueta impresa sea leible bindeando el <Return> a una funcion. Entonces tendria que hacer como en login: un if para mirar si estamos en esta pantalla y si es un usuario. Ten en cuenta que en cada lectura de etiqueta se ejecutaran las 2 funciones bindeadas pero como cada una está protegida por su if pues no pasa nada.
        pass

    def __submit_sample(self):
        # TODO: Ver si arduino está vivo; si no está pues enviar mensaje y poner problema por pantalla y que se le cerrará sesión y que vuelva mas tarde y tal.
        # TODO: En caso de arduino vivo: pedirle que abra la puerta (aun así con un timeout). Si salta el timeout hacer lo del if anterior, y si no salta pues llamar a incrementar variable muestras dadas + Registrar en las 2 BD (en la de muestras_saliva deberia haber por huevos un registro ya empezado y sin hora de entregar, ver que sea asi (en DBcontroller), aparte tendre que poner la diferencia entre la hora de recogidamuestra y la de entrega en la funcion esa de DBcontroller) + avisarle que ya puede entregar muestra en el lado + ActivePerson.getCurrent.set_has_submited_to_true() + volver al menú anterior después de unos segundos.
        pass

    def go_to_submitSample_screen(self):
        self.__current_step = 0
        self.__submitSampleScreen_frame.tkraise()
        messagebox.showwarning("INFORMACIÓN PREVIA", """Recuerda que para que la muestra de saliva sea válida, no debes haber ingerido nada en los últimos 30 minutos. \n
        En caso de que hayas comido o bebido algo hace menos de 30 minutos, cierra este mensaje, haz click en el botón de 'VOLVER ATRÁS' y después sal del programa (botón 'Cerrar Sesión'). \n
        Podrás volver a usar esta máquina más adelante, cuando hayan transcurrido 30 minutos desde la última ingesta""")