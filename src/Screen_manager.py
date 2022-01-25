from tkinter import *
import constants


root = None

def start_application():
    global root
    if root != None:
        raise Exception("You have already created an application")
    else:
        root = Tk()
        width = constants.SCREEN_WIDTH
        height = constants.SCREEN_HEIGHT
        root.geometry(str(width) + "x" + str(height))
        #root.config(cursor="none")
    return root

def get_root():
    global root
    if root == None:
        raise Exception("You have not created started the application yet")
    else: 
        return root

def init_screen_frame():
    global root
    if root == None:
        raise Exception("You need to start an application before creating frames")
    frame = Frame(root)
    frame.config(bg = "white")
    frame["width"]= constants.SCREEN_WIDTH 
    frame["height"] = constants.SCREEN_HEIGHT
    frame.grid(row=0, column=0, sticky='NSWE')
    return frame

def header_frame(parent_frame):
    header_f = Frame(parent_frame)
    header_f.config(bg = "#7BACFC")
    header_f["width"]= constants.SCREEN_WIDTH
    header_f["height"] = 1/4 * constants.SCREEN_HEIGHT 
    header_f.grid(row=0, column=0, sticky='NSWE')
    #header_f.columnconfigure(0,weight=3)
    #header_f.columnconfigure(1,weight=1)
    return header_f

def body_frame(parent_frame):
    body_f = Frame(parent_frame)
    body_f.config(bg = "white")
    body_f["width"]= constants.SCREEN_WIDTH
    body_f["height"] = 3/4 * constants.SCREEN_HEIGHT
    body_f.grid(row=1, column=0, sticky='NSWE')
    return body_f