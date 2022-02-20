import Screen_manager
import DBcontroller
import constants
from enum import Enum


#ENUM:
Language = Enum("Language", "SPANISH CATALAN ENGLISH")

str_to_index_map = {
    "bienvenido a SALIBANK" : 0,
    "instrucciones login" : 1,
    "cambiar idioma" : 2,
    "no puede iniciar sesion (cabecera)" : 3,
    "no puede iniciar sesion (cuerpo)" : 4,
    "identificacion erronea (cabecera)" : 5,
    "identificacion erronea (cuerpo)" : 6,
    "acceso denegado (cabecera)" : 7,
    "acceso denegado (cuerpo)" : 8,
    "introduce tu clave de acceso" : 9,
    "apagar" : 10,
    "el programa se cerrará y la máquina se apagará" : 11,
    "título administrador" : 12,
    "título operario" : 13,
    "texto botón cerrar sesión para admin/operador" : 14,
    "avisador etiquetas restantes" : 15,
    "avisador kits restantes" : 16,
    "avisador muestras entregadas" : 17,
    "de" : 18,
    "reponer kits" : 19,
    "reponer etiquetas" : 20,
    "recoger muestras" : 21,
    "consultar BD" : 22,
    "efectuar reposicion kits (cabecera)" : 23,
    "efectuar reposicion kits (cuerpo)" : 24,
    "efectuar recogida muestras (cabecera)" : 25,
    "efectuar recogida muestras (cuerpo)" : 26,
    "efectuar reposición etiquetas (cabecera)" : 27,
    "efectuar reposición etiquetas (cuerpo)" : 28,
    "kits repuestos (cabecera)" : 29,
    "muestras recogidas (cabecera)" : 30,
    "etiquetas repuestas (cabecera)" : 31,
    "reposicion/recogida finalizada (cuerpo)" : 32,
    "mensaje cierre sesión (cabecera)" : 33,
    "mensaje cierre sesión (cuerpo)" : 34,
    "título usuario" : 35,
    "texto botón cerrar sesión para usuario" : 36,
    "obtener un kit" : 37,
    "entregar una muestra" : 38,
    "¿qué hago?" : 39,
    "ayuda" : 40,
    "respuesta al ¿qué hago? (cabecera)" : 41,
    "respuesta al ¿qué hago? (cuerpo)" : 42,
    "base de datos:" : 43,
    "cambiar de base de datos" : 44,
    "volver atrás" : 45,
    "título obtener kit" : 46,
    "información previa (cabecera)" : 47,
    "quiero recoger un kit" : 48,
    "kit dispensado (cabecera)" : 49,
    "kit dispensado (cuerpo)" : 50,
    "paso número..." : 51,
    "botón siguiente" : 52,
    "botón imprimir etiqueta" : 53,
    "botón avisar muestra entregada" : 54,
    "aviso de muestra entregada (cabecera)" : 55,
    "aviso de muestra entregada (cuerpo)" : 56,
    "aviso de error de impresión (cabecera)" : 57,
    "aviso de error de impresión (cuerpo)" : 58,
    "información previa (recordatorio)" : 59,
    "información previa (extendida)" : 60,
    "error recogida kit (cabecera)" : 61,
    "error recogida kit (cuerpo)" : 62,
    "necesaria reposicion etiquetas (cabecera)" : 63,
    "necesaria reposicion etiquetas (cuerpo)" : 64,
    "comprobacion reposicion etiquetas (cabecera)" : 65,
    "comprobacion reposicion etiquetas (cuerpo)" : 66,
    "necesaria reposicion kits (cabecera)" : 67,
    "necesaria reposicion kits (cuerpo)" : 68,
    "comprobacion reposicion kits (cabecera)" : 69,
    "comprobacion reposicion kits (cuerpo)" : 70, 
    "necesario vaciado deposito muestras (cabecera)" : 71,
    "necesario vaciado deposito muestras (cuerpo)" : 72,
    "comprobacion vaciado deposito muestras (cabecera)" : 73,
    "comprobacion vaciado deposito muestras (cuerpo)" : 74,
    "título pestaña no disponible" : 75,
    "cerrar programa pestaña no disponible" : 76,
    "clave errónea" : 77
}

messages = []

def set_current_language(language):
    global messages
    if language == Language.SPANISH:
        messages = DBcontroller.get_messages(constants.SPANISH_LANGUAGE_PATH)
    elif language == Language.CATALAN:
        messages = DBcontroller.get_messages(constants.CATALAN_LANGUAGE_PATH)
    elif language == Language.ENGLISH:
        messages = DBcontroller.get_messages(constants.ENGLISH_LANGUAGE_PATH)
    else:
        Screen_manager.get_root().destroy()
        raise Exception(str(language) + " unsuported language")


def get_message(identifier_str):
    global messages
    if messages == []:  # Programmer forgot to set a default language at main.py. We set SPANISH as default
        set_current_language(Language.SPANISH)
    else:
        message_index = str_to_index_map.get(identifier_str, -1)
        if message_index == -1:
            Screen_manager.get_root().destroy()
            raise Exception(identifier_str + " is an invalid identifier_str for Language_controller")
        return messages[message_index]
        