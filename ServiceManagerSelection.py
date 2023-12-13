from WinServiceManager import WinServiceGui

from tkinter.ttk import Combobox
from tkinter import Tk, Frame, Label, Button, Entry, messagebox, W

from os import listdir
from os import path as osPath

from json import dump as jsDump
from json import load as jsLoad

class ServiceManagerSelection():
    def __init__(self) -> None:
        self.config_path = ".\\config.json" 
        
        try:
            with open(self.config_path,'r') as f:   # load config
                config = jsLoad(f)
                self.colors = config['colors']
                self.font = config['font']
                self.serviceListDir = config['serviceListDir']
                
        except FileNotFoundError:   # Config not found
            messagebox.showerror("Config not found","File config.json is not in the directory")
            exit()
            
        except KeyError:    # Error in Config File
            messagebox.showerror("Config failure","Config.json has errors in it")
            exit()

        ######
        # GUI
        ######
        self.serviceManagerSelectionWindow = Tk()
        self.serviceManagerSelectionWindow.title("ServiceManager")
        self.serviceManagerSelectionWindow.config(bg=self.colors['bg'])
        self.serviceManagerSelectionWindow.geometry("275x135")      

        new_b = Button(self.serviceManagerSelectionWindow, text="New", width=10, bg=self.colors['btn'], fg=self.colors['fg'], font=self.font, borderwidth=3, command=self.new_config)   # create new ServiceMap
        new_b.grid(row=0,column=0, pady=10, padx=10,sticky=W)
        
        Label(self.serviceManagerSelectionWindow, text="Select Config", bg=self.colors['bg'], fg=self.colors['fg'], font=self.font).grid(row=1,column=0)
    
        self.selection_c = Combobox(self.serviceManagerSelectionWindow) # select ServiceMap
        self.selection_c.grid(row=2, column=0, padx=5)
        self.refresh()  # load Servicemaps on start
        
        ok_b = Button(self.serviceManagerSelectionWindow, text="Run",width=10,bg=self.colors['btn'],fg=self.colors['fg'],font=self.font, borderwidth=3, command=self.select_conf)   # open ServiceManager with selection
        ok_b.grid(row=2, column=1, sticky=W)
        
        self.state_overview_l = Label(self.serviceManagerSelectionWindow, text="", fg=self.colors['fg'], bg=self.colors['bg'], font=self.font)
        self.state_overview_l.grid(row=3,column=0)
                
        self.serviceManagerSelectionWindow.mainloop()

    # gets Files from serviceListDir Folder
    def refresh(self): 
        if len(listdir(self.serviceListDir)) != 0:
            choices = [ele.replace('.json','') for ele in listdir(self.serviceListDir)] # creates list with alle Filenames without file ending
        else:
            choices = [""]
        self.selection_c.config(values=choices)
        self.selection_c.current(0) # default values = first item
    
    # opens the ServiceManagerGui with selected Service Map file        
    def select_conf(self):  
        fileName = self.selection_c.get()   # get selection
        hostpath = self.serviceListDir + '\\' + fileName + '.json'
        if osPath.isfile(hostpath):  # Check if File exists
            self.state_overview_l.config(text=fileName + " opened", fg=self.colors['state_run'])
            WinServiceGui(hostpath, self.config_path, fileName)
        else:
            self.state_overview_l.config(text="File not found", fg=self.colors['state_stop'])
            self.refresh()
    
    # opens Window to create a new ServiceMap
    def new_config(self):
        newConfWindow = Tk()
        newConfWindow.title("New Config")
        newConfWindow.config(bg=self.colors['bg'])
        
        self.serviceRow = 5 # start value for add Service (starts in row 5 because the other elements will take 4 rows)
        self.EntryList = [] # a empty list for the hostname and service entrys
        
        Label(newConfWindow, text="Name: ",bg=self.colors['bg'],fg=self.colors['fg'],font=self.font).grid(row=0,column=0,padx=10,pady=5)
        name_e = Entry(newConfWindow, font=self.font)
        name_e.grid(row=0,column=1,padx=10,pady=5)
        
        Label(newConfWindow, text="Autorefresh(y=yes,n=no):",bg=self.colors['bg'],fg=self.colors['fg'],font=self.font).grid(row=1,column=0,padx=10,pady=5)
        autoRef_e = Entry(newConfWindow, font=self.font)
        autoRef_e.grid(row=1,column=1,padx=10,pady=5)
        
        Label(newConfWindow, text="Refresh Time(s):",bg=self.colors['bg'],fg=self.colors['fg'],font=self.font).grid(row=2,column=0,padx=10,pady=5)
        refreshTime_e = Entry(newConfWindow, font=self.font)
        refreshTime_e.grid(row=2, column=1, padx=10,pady=5)
        
        Label(newConfWindow, text="Rows per Column:",bg=self.colors['bg'],fg=self.colors['fg'],font=self.font).grid(row=3, column=0,padx=10,pady=5)
        rowsPerCol_e = Entry(newConfWindow, font=self.font)
        rowsPerCol_e.grid(row=3, column=1,padx=10,pady=5)
        
        create_b = Button(newConfWindow, text="Create ServiceList",bg=self.colors['btn'],fg=self.colors['fg'],font=self.font, borderwidth=3, command=lambda: self.create_serviceList(name_e.get(), autoRef_e.get(), refreshTime_e.get(),rowsPerCol_e.get(),newConfWindow))  # Creates ServiceMap
        create_b.grid(row=self.serviceRow+1,column=1,padx=10,pady=5)
        
        self.state_add_l = Label(newConfWindow, text="", fg=self.colors['fg'], bg=self.colors['bg'], font=self.font)
        self.state_add_l.grid(row=self.serviceRow+1, column=0)
        
        addService_b = Button(newConfWindow, text="Add Service",bg=self.colors['btn'],fg=self.colors['fg'],font=self.font, borderwidth=3, command=lambda: self.add_service(newConfWindow,create_b)) #
        addService_b.grid(row=4, column=0, columnspan=2,padx=10,pady=5)
    
        newConfWindow.mainloop()
    
    # adds a new service Frame with 2 Entrys (hostname, servicename)    
    def add_service(self,window:Tk, create_b:Entry):
        service_f = Frame(window)
        service_f.config(bg=self.colors['bg'])
        service_f.grid(row=self.serviceRow,column=0, columnspan=3,padx=10,pady=5)
    
        Label(service_f, text="Hostname",bg=self.colors['bg'],fg=self.colors['fg'],font=self.font).grid(row=0,column=0)
        hostname_e = Entry(service_f, font=self.font)
        hostname_e.grid(row=0,column=1)
        
        Label(service_f, text="Service",bg=self.colors['bg'],fg=self.colors['fg'],font=self.font,).grid(row=0,column=2)
        service_e = Entry(service_f, font=self.font)
        service_e.grid(row=0,column=3)
        
        del_b = Button(service_f, text="X",bg=self.colors['state_stop'], fg=self.colors['fg'], font=self.font, borderwidth=0, command=lambda: self.del_service(service_f, [hostname_e, service_e]))  # deletes a service frame
        del_b.grid(row=0,column=4,padx=5)
        
        self.EntryList.append([hostname_e, service_e])  # appends the Entry list
        self.serviceRow += 1    # adds a row
        
        create_b.grid(row=self.serviceRow + 1)  # adds a row for the create button 
        self.state_add_l.grid(row=self.serviceRow + 1) # adds a row for the state label
    
    def del_service(self,frame:Frame, entrys:list): 
        frame.destroy() # delete service Frame
        if entrys in self.EntryList:    
            self.EntryList.remove(entrys)   # remove Entrys from EntryList
    
    # create ServiceMap
    def create_serviceList(self, name:str, autoRef:str, refreshTime:str, rowsPerCol:str, window:Tk):
        if self.EntryList == []:    # Check is services added
            self.state_add_l.config(text='no hosts an services entered', fg=self.colors["state_stop"])
            return False
        
        if name == "" or autoRef == "" or refreshTime == "" or rowsPerCol == "":    # check if name, autoref, refreshtime, rowsPerCol are entered
            self.state_add_l.config(text='no name, autoRef or Refreshtime entered', fg=self.colors["state_stop"])
            return False
        
        if autoRef.lower() not in ['y','n']:    # check if autoref is y or n 
            self.state_add_l.config(text='autoRef only allows "y" or "n"', fg=self.colors["state_stop"])
            return False
        
        autoRef = True if autoRef.lower() == 'y' else False # Set the bool state for the ServiceMap

        try:    # try to convert refreshTime and rowsPerCol to int
            refreshTime = int(refreshTime)  
            rowsPerCol = int(rowsPerCol)
        except ValueError:
            self.state_add_l.config(text='Wrong Entry(check RefreshTime a. RowsPerCol int)', fg=self.colors["state_stop"])
            return False  
          
        hostOut = {}    # generate host dict
        for e in self.EntryList:
            hostname = e[0].get()
            service = e[1].get()
        
            if hostname == "" or service == "": # check if host and service is entered
                self.state_add_l.config(text='Check Hostnames and Servicenames', fg=self.colors["state_stop"])
                return False
            
            if hostname in hostOut: # if one host has n services / check if its already in the list and append
                hostOut[hostname] = hostOut[hostname] + [service]
            else:   # create new host
                hostOut[hostname] = [service]
        
        output = {} # create output dict for json
        output["hosts"] = hostOut
        output["autoRefresh"] = autoRef
        output["refreshTimeSeconds"] = refreshTime   
        output["rowsPerColumn"] = rowsPerCol

        with open(self.serviceListDir + f"\\{name}.json","w") as f:
            jsDump(output,f)    # write json and save it to serviceListDir
         
        window.destroy()    # delete window
        self.refresh()      # refresh the Selection Window

if __name__ == '__main__':
    ServiceManagerSelection()
