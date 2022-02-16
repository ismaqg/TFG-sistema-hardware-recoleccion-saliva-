import Screen_manager
from enum import Enum


#ENUM:
Language = Enum("Language", "SPANISH CATALAN ENGLISH")


def set_current_language(language):
    if language == Language.SPANISH:
        #TODO
        pass
    elif language == Language.CATALAN:
        #TODO
        pass
    elif language == Language.ENGLISH:
        #TODO
        pass
    else:
        Screen_manager.get_root().destroy()
        raise Exception(str(language) + " Unsuported language")


def get_message(identifier):
    #TODO
    pass
        