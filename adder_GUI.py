from tkinter import *
from PIL import ImageTk, Image
import threading
from spotify_extract import *


class GUI:
    
    def __init__(self, song_comms):
        self.root = Tk()
        #Testing with using a Queue
        self.song_comms = song_comms
        #Make the App window
        self.root.geometry('720x480')
        self.root.iconbitmap('resources/maple_leaf.ico')
        self.root.title('SpotifyQueueAdder')
        
        #Make Start Button
        #############################################
        self.start_frame = LabelFrame(self.root)
        self.start_frame.grid(row=0,column=0,sticky=EW)
        self.start_but = Button(self.start_frame, 
                                   text='Click Here to Start Building', 
                                   command=self.start_func, state=DISABLED)
        self.start_but.pack(fill='both')
        #############################################
    
        #Make Debug button
        #############################################
        self.debug_frame = LabelFrame(self.root)
        self.debug_frame.grid(column=1,row=0,sticky=EW)
        self.debug_but = Button(self.debug_frame, 
                                   text='Click here to set DEBUG mode', 
                                   command=self.debug_time)     
        self.debug_but.pack(fill='both')
        self.debug_label_frame = LabelFrame(self.root)
        self.debug_label_frame.grid(column=1,row=1, sticky=EW)
        self.debug_label = Label(self.debug_label_frame, text="Debug disabled, time bewteen scans: 30 Seconds")
        self.debug_label.pack()
        #############################################
        
        #Debug Check Button
        #############################################
        self.check_frame = LabelFrame(self.root)
        self.check_frame.grid(column=0,row=2, sticky=EW)
        self.check_but = Button(self.check_frame, 
                                   text='Click here to enable Start', 
                                   command=lambda:self.enable_but(self.start_but, [self.debug_but, self.check_but]))
        self.check_but.grid(column=0,row=0,sticky=EW)
        self.check_lab = Label(self.check_frame, 
                               text='Doing so disables the ability for DEBUG mode',pady=10)
        self.check_lab.grid(column=0,row=1)  
        #############################################
        
        #Invis sections
        #############################################
        self.ID_lab = Label(self.root, text='')
        self.ID_lab.grid(column=1,row=2, sticky=EW)
        self.ID_but_lab = Label(self.root, text='')
        self.ID_but_lab.grid(column=1,row=3)
        
        #Make Exit Button
        #############################################
        self.exit_frame = LabelFrame(self.root)
        self.exit_frame.grid(columnspan=2,sticky=EW)
        self.exit_button = Button(self.exit_frame, 
                                  text='Click Here to Exit', 
                                  command=self.root.quit)
        self.exit_button.pack(fill='both')
        self.root.after(func=self.read_queue(),ms=2000)
        self.root.mainloop()
        #############################################
        
    def start_func(self):
        self.build_label = Label(self.root, text="Building...")
        self.build_label.grid(column=0,row=1, sticky=EW)
        threading.Thread(target=begin, args=(self.song_comms,) ,daemon=True).start()
        self.disable_but(self.start_but)
        
    def debug_time(self):
        global SLEEP_TIME
        
        self.disable_but(self.debug_but)
        self.disable_but(self.check_but)
        self.enable_but(self.start_but)
        self.debug_label.destroy()
        self.debug_label = Label(self.debug_label_frame, anchor=NW, justify=LEFT,text="Debug enabled, time bewteen scans: 5 Seconds")
        self.debug_label.pack()
        self.build_label = Label(self.root, text="Start is now enabled")
        self.build_label.grid(column=0,row=1, sticky=EW)
        self.send_queue('Set DEBUG')
    
    def disable_but(self, but):
        if but['state'] == NORMAL or but['state'] == ACTIVE:
            but['state'] = DISABLED
    
    def enable_but(self, but, dis = None):
        if but['state'] == DISABLED:
            but['state'] = NORMAL
        if dis != None:
            for but in dis:
                self.disable_but(but)
    
    def send_queue(self,val):
        self.song_comms.put(val)
        
    def read_queue(self):
        try:
            request = self.song_comms.get_nowait()
            self.interp_request(request)
        except Empty:
            pass
        self.root.after(func=self.read_queue,ms=2000)
    
    def interp_request(self, request):
        if request == 'ID':
            self.get_ID()
        else:
            pass
    
    def get_ID(self):
        ent_ID = Entry(self.root,
            width=50,
            borderwidth=5)
        ent_ID.insert(0,'Type Google Sheet ID here')
        ent_ID.grid(column=1,row=2, sticky=EW)
        ID_but = Button(self.root, text="Submit ID",  
                            command=lambda: self.send_queue(ent_ID.get()), 
                            fg='red', bg='white')
        ID_but.grid(column=1,row=3)

if __name__ == '__main__':
    song_comms = Queue()
    test = GUI(song_comms)
    

    