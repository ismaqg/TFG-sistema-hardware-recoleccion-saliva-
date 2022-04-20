from tkinter import *
import Screen_manager
import signal
import constants


class GIF:

    def __init__(self, GIF_path):

        # create the frame and the label where the GIF will be contained
        self.__GIF_container_container = Screen_manager.init_screen_frame()  # frame to contain the label with the GIF.
        self.__GIF_container_container.rowconfigure(0, weight=1)
        self.__GIF_container_container.columnconfigure(0, weight=1)
        self.__GIF_container = Label(self.__GIF_container_container, image = '')  # without starting image. The starting image will be given in the animate_gif function
        self.__GIF_container.grid(row = 0, column = 0, sticky = 'NSEW')

        # Load the different photograms of the GIF in one list:
        frame_index = 0
        self.__framelist = []
        while True:
            try: # read a frame from gif file
                self.__frame = PhotoImage(file = GIF_path, format = "gif -index " + str(frame_index))  # takes a certain "fotogram" of the GIF, given the index of the photogram that we want. THIS LINE THROWS AN EXCEPTION IF THE INDEX IS OUT OF RANGE (greather than the number of photograms-1)
                self.__framelist.append(self.__frame)
                frame_index += 1
            except:  # The first line of "try" is throwing an exception if the index of the GIF photogram doesn't exist. Note that we are iterating until this happens because we don't know how much photograms has the GIF that we are using (in this case is 30, but we can use other GIFs with this program)
                self.__last_frame_index = frame_index - 1  # save index for last frame. Used in the "animate gif" function
                break  # break while loop


    def start_gif(self):
        #self.__GIF_container_container.grid(row = 0, column = 0, sticky='NSEW')  # because we do "grid_forget" in the stop_gif function
        self.__GIF_container_container.tkraise()  # to put it in the front of the view
        self.__index = 0  # used to track the index in the framelist of the current photogram that we have to show
        signal.signal(signal.SIGALRM, self.__animate_gif)
        signal.setitimer(signal.ITIMER_REAL, 0.000001, 0.05)  # que salte a la funcion __animate_gif() despues de 1us y que luego esté todo el rato saltando a ella cada 0.5s


    # PRE: Se ha tenido que hacer start_gif previamente
    def stop_gif(self):
        self.__GIF_container_container.grid_forget()
        signal.setitimer(signal.ITIMER_REAL, 0)  # cancel the timer


    def __animate_gif(self, signum, sigframe):  # ignore the signum and sigframe (are implicits in SIGALARM when alarm raises)
        self.__GIF_container.config(image = self.__framelist[self.__index])  # it puts a certain photogram of the GIF on the label
        print("llega")
        self.__index += 1
        if self.__index > self.__last_frame_index:
            self.__index = 0
        
        #self.__anim = Screen_manager.get_root().after(50, lambda:self.__animate_gif(index))

