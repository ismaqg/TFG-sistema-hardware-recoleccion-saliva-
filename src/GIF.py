from tkinter import *
from turtle import width
import Screen_manager
import constants


# global variables for GIF:
framelist = []  # list with the different photograms of the GIF
last_frame_index = 0
anim = None  # identifier of the "after" function return value
GIF_container = None  # Tkinter label (containing the GIF)
GIF_container_container = None  # Tkinter frame (containing the label which contains the GIF)


def __animate_gif(index):
    global anim, last_frame_index, framelist, GIF_container
    GIF_container.config(image = framelist[index])  # it puts a certain photogram of the GIF on the label
    index += 1
    if index > last_frame_index:
        index = 0
    anim = Screen_manager.get_root().after(50, lambda:__animate_gif(index))   # it puts a the next photogram of the GIF in the label after 50ms


def start_gif(GIF_path):
    # INIT GIF INFO:
    # count all frames in gif and save in list:
    global last_frame_index, framelist
    frame_index = 0
    while True:
        try: # read a frame from gif file
            frame = PhotoImage(file = GIF_path, format = "gif -index " + str(frame_index))  # takes a certain "fotogram" of the GIF, given the index of the photogram that we want. THIS LINE THROWS AN EXCEPTION IF THE INDEX IS OUT OF RANGE (greather than the number of photograms-1)
            framelist.append(frame)
            frame_index += 1
        except:  # The first line of "try" is throwing an exception if the index of the GIF photogram doesn't exist. Note that we are iterating until this happens because we don't know how much photograms has the GIF that we are using (in this case is 30, but we can use other GIFs with this program)
            last_frame_index = frame_index - 1  # save index for last frame. Used in the "animate gif" function
            break  # break while loop
    # label to show gif:
    global GIF_container, GIF_container_container
    GIF_container_container = Screen_manager.init_screen_frame()  # frame to contain the label with the GIF.
    GIF_container = Label(GIF_container_container, image = '')  # without starting image. The starting image will be given in the animate_gif function
    GIF_container.grid(row = 0, column = 0, sticky = 'NSEW')
    GIF_container_container.tkraise()  # show the frame containing the label with the GIF above all the other widgets of the application
    # START GIF ANIMATION
    __animate_gif(0)


# PRE: Some gif has been started
def stop_gif():
    global anim, GIF_container, GIF_container_container, framelist
    Screen_manager.get_root().after_cancel(anim)
    GIF_container_container.destroy()
    framelist.clear()
