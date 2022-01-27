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
    frame = Frame(root, bg = "white", width = constants.SCREEN_WIDTH, height = constants.SCREEN_HEIGHT)
    frame.grid(row = 0, column = 0, sticky='NSEW') # sticky='NSWE': stick in all the walls of its container
    frame.grid_propagate(False) # don't propagate the grid information to its childrens
    return frame

def header_frame(parent_frame):
    header_f = Frame(parent_frame, bg = constants.CATSALUT_COLOR, width = constants.SCREEN_WIDTH, height = 1/4 * constants.SCREEN_HEIGHT)
    header_f.grid(row=0, sticky='NSEW')
    header_f.grid_propagate(False)
    return header_f

def body_frame(parent_frame):
    body_f = Frame(parent_frame, bg = "white", width = constants.SCREEN_WIDTH, height = 3/4 * constants.SCREEN_HEIGHT)
    body_f.grid(row=1, sticky='NSEW')
    body_f.grid_propagate(False)
    return body_f