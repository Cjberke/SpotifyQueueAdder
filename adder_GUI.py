from tkinter import *
from PIL import ImageTk, Image
import threading
from spotify_extract import *

class GUI:
    
    def __init__(self):
        self.root = Tk()

        #Make the App window
        self.root.geometry('720x480')
        self.root.iconbitmap('resources/maple_leaf.ico')
        self.root.title('SpotifyQueueAdder')
    
        #Make Debug button
        self.debug_frame = LabelFrame(self.root, padx=15,pady=15)
        self.debug_frame.grid(column=0,row=0)
        self.debug_but = Button(self.debug_frame, 
                                   text='Click here to set DEBUG mode', 
                                   command=self.debug_time)     
        self.debug_but.pack()  
    
        #Make Start Button
        self.start_frame = LabelFrame(self.root, padx=25,pady=25)
        self.start_frame.grid(column=1,row=0)
        self.start_but = Button(self.start_frame, 
                                   text='Click Here to Start Building', 
                                   command=self.test_func)
        self.start_but.pack()
        self.start_label = Label(self.root, text='')
        self.start_label.grid(column=1,row=1)
    
        #Make Exit Button
        self.exit_frame = LabelFrame(self.root, padx=10,pady=10)
        self.exit_frame.grid(column=0,row=2)
        
        self.exit_button = Button(self.exit_frame, 
                                  text='Click Here to Exit', 
                                  command=self.root.quit)
        self.exit_button.pack()
        self.root.mainloop()
    
    def test_func(self):
        self.build_label = Label(self.root, text="Building...")
        self.build_label.grid(column=1,row=1)
        threading.Thread(target=begin, daemon=True).start()
        self.start_but['state'] = DISABLED
        
    def debug_time(self):
        global SLEEP_TIME
        self.debug_but['state'] = DISABLED
        self.debug_label = Label(self.root, text="Sleep time between scans: 5 Second")
        self.debug_label.grid(column=0,row=1)
        SLEEP_TIME = 5
        

if __name__ == '__main__':
    test = GUI()
    

    