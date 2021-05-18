from tkinter import *
from PIL import ImageTk, Image

class GUI:
    
    def __init__(self):
        self.root = Tk()
        self.make_window()
        self.debug_button()
        self.start_button()
        self.stop_button()
        self.root.mainloop()

    def make_window(self):
        self.root.geometry('720x480')
        self.root.iconbitmap('resources/maple_leaf.ico')
        self.root.title('SpotifyQueueAdder')
    
    def debug_button(self):
        self.debug_frame = LabelFrame(self.root, padx=15,pady=15)
        self.debug_frame.grid(column=0,row=0)
        self.debug_but = Button(self.debug_frame, 
                                   text='Click here to set DEBUG mode', 
                                   command=self.debug_time)     
        self.debug_but.pack()  
    
    def start_button(self):
        self.start_frame = LabelFrame(self.root, padx=25,pady=25)
        self.start_frame.grid(column=1,row=0)
        self.start_but = Button(self.start_frame, 
                                   text='Click Here to Start Building', 
                                   command=self.test_func)
        
        self.start_but.pack()
        self.start_label = Label(self.root, text='')
        self.start_label.grid(column=1,row=1)
    
    def stop_button(self):
        self.exit_frame = LabelFrame(self.root, padx=10,pady=10)
        self.exit_frame.grid(column=0,row=2)
        
        self.exit_button = Button(self.exit_frame, 
                                  text='Click Here to Exit', 
                                  command=self.root.quit)
        self.exit_button.pack()
    
    def test_func(self):
        self.build_label = Label(self.root, text="Building...")
        self.build_label.grid(column=1,row=1)
        self.start_but['state'] = DISABLED
        
    def debug_time(self):
        self.debug_but['state'] = DISABLED
        self.debug_label = Label(self.root, text="Sleep time between scans: 5 Second")
        self.debug_label.grid(column=0,row=1)
        #SLEEP_TIME = 5
        

if __name__ == '__main__':
    test = GUI()
    

    