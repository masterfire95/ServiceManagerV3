from WinService import WinService

from tkinter import Tk, Button, Label, Frame, messagebox, E, W
from threading import Thread
from json import load as jsLoad

class WinServiceGui():
    def __init__(self, host_path:str, config_path:str, windowName:str) -> None:
        with open(config_path,'r') as f:
            config = jsLoad(f)
            self.colors = config['colors']
            self.font = config['font']
            self.font_bold = config['font_bold']
        
        try:
            with open(host_path,'r') as f:
                hosts = jsLoad(f)
                self.hostList = hosts['hosts']
                self.autoRefreshState = hosts['autoRefresh']
                self.refreshTime = hosts['refreshTimeSeconds'] * 1000
                self.rows = hosts['rowsPerColumn']
                
        except FileNotFoundError:   # Config not found 
            messagebox.showerror("ServiceMap not found",f"{host_path} not found")
            exit()
            
        except KeyError:    # Error in Config File
            messagebox.showerror("ServiceMap failure",f"{host_path} has errors in it")
            exit()
                
        self.main_service_window = Tk()
        self.main_service_window.title(windowName + " - Services")
        self.main_service_window.config(background=self.colors['bg'])
        
        self.service_elements = self.gen_frames()
            
        ref_b = Button(self.main_service_window, width=20, text="Refresh",bg=self.colors['bg'], fg=self.colors['fg'], font=self.font, command= lambda: Thread(target=self.refresh).start())
        ref_b.grid(row=0, column=0, pady=10)
        
        Thread(target=self.refresh).start()
        
        if self.autoRefreshState:
            self.main_service_window.after(self.refreshTime, self.autoRefresh)  
        
        self.main_service_window.mainloop()
        
    def gen_frames(self):
        service_elements = []
        row = 1
        col = 0
        for host,services in self.hostList.items():
            for service in services:
                if row == self.rows:
                    row = 1
                    col += 1
                    
                service_f = Frame(self.main_service_window, bg=self.colors['bg'], borderwidth=2, relief='groove')
                service_f.grid(row=row, column=col,padx=10, pady=10)
                
                Label(service_f, text=host, bg=self.colors['bg'], fg=self.colors['fg'], font=self.font_bold).grid(row=0, column=0, columnspan=2)
                Label(service_f,text=service,bg=self.colors['bg'], fg=self.colors['fg'], font=self.font).grid(row=1, column=0, columnspan=2)
                state_l = Label(service_f, text=f'State : unkown', fg='orange', bg=self.colors['bg'], font=self.font_bold)
                state_l.grid(row=2,column=0,columnspan=2)
                            
                start_b = Button(service_f, text="Start", width=15, bg=self.colors['bg'], fg=self.colors['fg'], font=self.font, command=lambda host=host, service=service: Thread(target=self.start_service,args=(host, service,)).start())
                start_b.grid(row=3, column=0, columnspan=1, pady=5, padx=5, sticky=E)
                
                stop_b = Button(service_f, text="Stop", width=15, bg=self.colors['bg'], fg=self.colors['fg'], font=self.font, command=lambda host=host, service=service: Thread(target=self.stop_service,args=(host, service,)).start())
                stop_b.grid(row=3, column=1, columnspan=1, pady=5, padx=5, sticky=W)
                
                service_elements.append([host, service, state_l])   
                row += 1
        
        return service_elements
    
    def autoRefresh(self):
        Thread(target=self.refresh).start()
        self.main_service_window.after(self.refreshTime, self.autoRefresh)
        
    def refresh(self):               
        for host in self.service_elements:
            state = WinService.check_state_single_host(host[0],[host[1]])
            service_state = []
            if state[0][2] == 1: service_state = ["Stopped",self.colors['state_stop']]
            elif state[0][2] == 2: service_state = ["Starting",self.colors['state_pend']]
            elif state[0][2] == 3: service_state = ["Stopping",self.colors['state_pend']]
            elif state[0][2] == 4: service_state = ["Running",self.colors['state_run']]
            else: service_state = ["Unknown",self.colors['state_unkown']]
            host[-1].config(text=service_state[0],fg=service_state[1])
            
    def start_service(self, hostName, service):
        WinService.start_service_single_host(hostName, service)
        Thread(target=self.refresh).start()
    
    def stop_service(self, hostName, service):
        WinService.stop_service_single_host(hostName, service)
        Thread(target=self.refresh).start()

if __name__ == '__main__':
    WinServiceGui()
