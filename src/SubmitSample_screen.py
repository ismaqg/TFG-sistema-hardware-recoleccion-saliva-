from tkinter import *
from tkinter import messagebox

import time

import Screen_manager
import constants
import Checker
import Arduino_controller
import Counters
import DBcontroller
from Person import ActivePerson

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
            self.__current_step = 1

            self.__submitSampleScreen_frame = Screen_manager.init_screen_frame()
            self.__submitS_header_frame = Screen_manager.header_frame( self.__submitSampleScreen_frame)
            self.__submitS_body_frame = Screen_manager.body_frame( self.__submitSampleScreen_frame)

            self.__title = Label(self.__submitS_header_frame, text = "ENTREGAR MUESTRA", bg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_TITLE_TEXT_SIZE, 'bold'))
            self.__return_b = Button(self.__submitS_header_frame, text = "VOLVER\nATRÁS", borderwidth=5, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__previous_screen)

            self.__title.grid(row = 0, column = 0, sticky = 'NSEW')
            self.__return_b.grid(row = 0, column = 1, sticky = 'NSEW', pady=10, padx=10)

            self.__submitS_header_frame.columnconfigure(0, weight=5)
            self.__submitS_header_frame.columnconfigure(1, weight=1)
            self.__submitS_header_frame.rowconfigure(0, weight=1)  # it's necessary to give a weight (even though there is only one row in clamKitscreen_header_frame) for sticky=NSEW of the inside widgets to work correctly


            self.__info_steps_title = Label(self.__submitS_body_frame, text = "PASO 1:", bg = "white", fg = constants.CATSALUT_COLOR, font = (constants.CATSALUT_TEXT_FONT, constants.SCREEN_SECOND_TITLE_TEXT_SIZE, 'bold'))
            self.__info_steps_displayer = Canvas(self.__submitS_body_frame)
            self.__next_step_b = Button(self.__submitS_body_frame, text = "SIGUIENTE", borderwidth=3, font = (constants.CATSALUT_TEXT_FONT, constants.BUTTON_TEXT_SIZE, 'bold'), command = self.__next_step_actions)

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


    # TODO: Algunos comentarios de aquí abajo los tendré que cambiar si al final las compuertas no son abiertas y cerradas por un arduino
    """
    STEP 1: Show the first instruction -> Salivate and spit in the big tube. The necessary of this step is done in go_to_submitSample_screen, not in next_step_actions.
    STEP 2: Show the 2nd instruction -> transfer saliva to small tube.
    STEP 3: Says that the next thing will be to print the identifier. The button in this step is "print label" but the printing is done during the next step
    STEP 4: While the printing is being done, this step shows how to stick the label and ask to stick like the image. When the printing has finished, the "next" button is enabled
    STEP 5: Says that a comprobation of the label sticked correctly is needed, so the user needs to pass the label through the label reader. When the reader reads the correct code, the "next" button is enabled
    STEP 6: Show the next instruction -> Clean the tube. And that the gate is going to start opening when clicking
    STEP 7: It says to deliver the tube at the gate that has just openned, and press "Entregado" when done. The button is disabled until the door is opened
    STEP 8: It's not a step as such. If we are here we know that all of the above steps have already been completed, so in this point the user will be logged out
    """
    def __next_step_actions(self):

        # TODO in step 5: aqui puedo comprobar que la etiqueta impresa sea leible bindeando el <Return> a una funcion. Entonces tendria que hacer como en login: un if para mirar si estamos en esta pantalla (en submit screen) y si es un usuario (Y TAMBIEN SI EL PASO ACTUAL ES EL 5). Ten en cuenta que en cada lectura de etiqueta se ejecutaran las 2 funciones bindeadas pero como cada una está protegida por su if pues no pasa nada.
        # TODO EN EL PASO 5 CADA VEZ QUE SE LEA ALGO INCORRECTO, SE PONDRA UN ERROR POR PANTALLA DE QUE NO ESTÁS LEYENDO LA ETIQUETA QUE TOCA O QUE NO ESTÁ BIEN PEGADA, QUE SI NO LO CONSIGUES LEER VUELVAS AL MENÚ PRINCIPAL PARA VOLVER A PEDIR OTRA ETIQUETA QUE PEGARÁS ENCIMA

        self.__current_step += 1

        if self.__current_step == 8: # It will be entered here when the action of the last step (step 7: deliver the sample) has been completed (i.e. THE SAMPLE HAS BEEN SUBMITTED)
            self.__sample_submitted()

        self.__info_steps_title["text"] = "PASO " + str(self.__current_step)
        # TODO: Añadir la imagen del step que toque al canva al canva (tranquilo que no hay que hacer 7 ifs. A las imagenes las voy a llamar step1, step2, etc. Por lo que puedo conseguir la imagen que toca porque sé el valor de current_step)

        # Change the text of the button of this step and make the actions associated, if any:
        if self.__current_step in {2, 5, 6}: 
            self.__next_step_b["text"] = "SIGUIENTE"
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 3:
            self.__next_step_b["text"] = "IMPRIMIR ETIQUETA"
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 4:
            self.__next_step_b["text"] = "SIGUIENTE"
            self.__next_step_b["state"] = DISABLED
            # TODO: Añadir el codigo especial del paso de imprimir etiqueta (cuando se acabe la impresion el boton se pondra enabled). Ten en cuenta de mirar si está viva, si quedan etiqutas, añadir info a las BDs (evento + ID_etiqueta), etc. Borrar el siguiente codigo que es provisional:
            time.sleep(4)
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 5:
            self.__next_step_b["text"] = "SIGUIENTE"
            self.__next_step_b["state"] = DISABLED
            # TODO: aqui que el bind con <return> ya haga caso y cuando se vea que la etiqueta se puede leer pues se pondra en ENABLED el boton de siguiente. Nota: en la comprobacion de la etiqueta leida hay que mirar que el input se haya hecho en el paso 5 obviamente. Borrar el siguiente codigo que es provisional:
            time.sleep(4)
            self.__next_step_b["state"] = NORMAL
        elif self.__current_step == 7:
            self.__next_step_b["text"] = "ENTREGADO"
            self.__next_step_b["state"] = DISABLED
            self.__open_submit_gate()  # TODO: Si al final no hay que abrir una compuerta a través del arduino, quitar esto que no tendría sentido
            self.__next_step_b["state"] = NORMAL

 
    def __open_submit_gate(self):  # TODO: Si al final no hay que abrir una compuerta a través del arduino, quitar esto que no tendría sentido
        if (Checker.is_arduino_alive()):

            # TODO: Pedirle al arduino que abra la compuerta y programar un timeout que puede saltar si tarda mucho
    
            time.sleep(4) # TODO: borrar este sleep, está emulando la apertura de la puerta que aún no está
        else:
            Arduino_controller.inoperative_arduino_actions()
        

    def __sample_submitted(self):
        if (Checker.is_arduino_alive()):  # TODO: LEE ENTERO: Si al final no hay que cerrar ninguna compuerta con el arduino. borrar esta línea que no tendría sentido. SALVO QUE AL FINAL UTILICEMOS UN ARDUINO AHÍ PARA MEDIR LA TEMPERATURA O ALGO DEL ESTILO
            Counters.increment_stored_samples()
            DBcontroller.add_new_event(ActivePerson.getCurrent().get_CIP(), "SAMPLE SUBMITTED")  # to info_uso DB
            DBcontroller.add_sample_submission()  # to muetras_saliva DB
            ActivePerson.getCurrent().set_has_submitted_to_true()
            messagebox.showinfo("MUESTRA ENTREGADA", "La muestra ha sido entregada. Haz click sobre 'OK' para ser desconectado correctamente de la aplicación")
            ActivePerson.getCurrent().logOut()

            # TODO: En caso de que sea el arduino el que abre y cierra puera, aquí tengo que cerrarla. Poner un timeout por si el arduino dejase de funcionar aquí (y si salta el timeout, ir a la pantalla de Not_available)
    
        else:
            Arduino_controller.inoperative_arduino_actions()



    def go_to_submitSample_screen(self):
        self.__current_step = 1
        # TODO: Añadir la imagen del step 1 al canva
        self.__next_step_b["text"] = "SIGUIENTE"
        self.__next_step_b["state"] = NORMAL
        self.__info_steps_title["text"] = "PASO 1"
        self.__submitSampleScreen_frame.tkraise()
        messagebox.showwarning("INFORMACIÓN PREVIA", """Recuerda que para que la muestra de saliva sea válida, no debes haber ingerido nada en los últimos 30 minutos. \n
        En caso de que hayas comido o bebido algo hace menos de 30 minutos, cierra este mensaje, haz click en el botón de 'VOLVER ATRÁS' y después sal del programa (botón 'Cerrar Sesión'). \n
        Podrás volver a usar esta máquina más adelante, cuando hayan transcurrido 30 minutos desde la última ingesta""")