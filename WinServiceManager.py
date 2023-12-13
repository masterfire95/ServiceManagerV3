from datetime import datetime

from WinService import WinService

from tkinter import Tk, Button, Label, Frame, messagebox, E, W
from threading import Thread
from json import load as jsLoad

class WinServiceGui():
    def __init__(self, host_path:str, config_path:str, windowName:str) -> None:
        with open(config_path,'r') as f:    # load config
            config = jsLoad(f)
            self.colors = config['colors']
            self.font = config['font']
            self.font_bold = config['font_bold']
        
        try:
            with open(host_path,'r') as f:  # load host file
                hosts = jsLoad(f)
                self.hostList = hosts['hosts']
                self.autoRefreshState = hosts['autoRefresh']
                self.refreshTime = hosts['refreshTimeSeconds'] * 1000   # seconds to milliseconds
                self.rows = hosts['rowsPerColumn'] + 1  # for row grid
                
        except FileNotFoundError:   # Servicemap not found not found 
            messagebox.showerror("ServiceMap not found",f"{host_path} not found")
            exit()
            
        except KeyError:    # Error in Servicemap File
            messagebox.showerror("ServiceMap failure",f"{host_path} has errors in it")
            exit()
                
        self.main_service_window = Tk()
        self.main_service_window.title(windowName + " - Services")
        self.main_service_window.config(background=self.colors['bg'])
        
        self.service_elements = self.gen_frames()   # gen. Frames
            
        ref_b = Button(self.main_service_window, width=20, text="Refresh",bg=self.colors['btn'], fg=self.colors['fg'], font=self.font, borderwidth=3, command= self.refresh) # refresh btn
        ref_b.grid(row=0, column=0, pady=10)
        
        self.ref_l = Label(self.main_service_window, text="", bg=self.colors['bg'], fg=self.colors['fg'], font=self.font)
        self.ref_l.grid(row=0, column=1)
        
        self.refresh() # refresh on startup
        
        if self.autoRefreshState:   # if autorefresh is on
            self.main_service_window.after(self.refreshTime, self.autoRefresh)  
                
        self.main_service_window.mainloop()
        
    def gen_frames(self):
        service_elements = []   # List for output entries
        row = 1
        col = 0
        for host,services in self.hostList.items():
            for service in services:
                if row == self.rows:    # reset rows and add column
                    row = 1
                    col += 1
                    
                service_f = Frame(self.main_service_window, bg=self.colors['frame'], borderwidth=3, relief='groove')
                service_f.grid(row=row, column=col,padx=10, pady=10)
                
                Label(service_f, text=host, bg=self.colors['frame'], fg=self.colors['fg'], font=self.font_bold).grid(row=0, column=0, columnspan=2)
                Label(service_f,text=service,bg=self.colors['frame'], fg=self.colors['fg'], font=self.font).grid(row=1, column=0, columnspan=2)
                state_l = Label(service_f, text=f'State : unkown', fg='orange', bg=self.colors['frame'], font=self.font_bold)
                state_l.grid(row=2,column=0,columnspan=2)
                            
                start_b = Button(service_f, text="Start", width=15, bg=self.colors['btn'], activebackground=self.colors['state_run'], fg=self.colors['fg'], font=self.font, borderwidth=3, command=lambda host=host, service=service: self.start_service(host,service))# Thread(target=self.start_service,args=(host, service,)).start()) # host=host, service=service => take host,service by creation not the current one in the loop
                start_b.grid(row=3, column=0, columnspan=1, pady=5, padx=5, sticky=E)
                
                stop_b = Button(service_f, text="Stop", width=15, bg=self.colors['btn'], activebackground=self.colors['state_stop'], fg=self.colors['fg'], font=self.font, borderwidth=3, command=lambda host=host, service=service:self.stop_service(host,service)) # Thread(target=self.stop_service,args=(host, service,)).start())
                stop_b.grid(row=3, column=1, columnspan=1, pady=5, padx=5, sticky=W)
                
                service_elements.append([host, service, state_l])   
                row += 1
        
        return service_elements
    
    def autoRefresh(self):
        self.refresh()
        self.main_service_window.after(self.refreshTime, self.autoRefresh)  # refresh after refreshTime
        
    def refresh(self):        
        for host in self.service_elements:           
            Thread(target=self.set_state_for_host,args=(host,)).start() # create parallelism
        
        now = datetime.now().strftime('%H:%M:%S')
        self.ref_l.config(text="last refresh: " + now,fg=self.colors['state_run'])
    
    def set_state_for_host(self,host):
        state = WinService.check_state_single_host_service(host[0],host[1])   # check state of windows service on host
        service_state = []
        if state[0][2] == 1: service_state = ["Stopped",self.colors['state_stop']]
        elif state[0][2] == 2: service_state = ["Starting",self.colors['state_pend']]
        elif state[0][2] == 3: service_state = ["Stopping",self.colors['state_pend']]
        elif state[0][2] == 4: service_state = ["Running",self.colors['state_run']]
        else: service_state = ["Unknown",self.colors['state_unkown']]
        host[-1].config(text=service_state[0],fg=service_state[1])
 
    def start_service(self, hostName, service):
        Thread(target=WinService.start_service_single_host,args=(hostName, service,)).start() # start Service
        self.refresh()
    
    def stop_service(self, hostName, service):
        Thread(target=WinService.stop_service_single_host,args=(hostName, service,)).start() # stop service
        self.refresh()

if __name__ == '__main__':
    pass