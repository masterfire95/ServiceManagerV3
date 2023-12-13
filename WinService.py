# Service = State 1 = stopped / 2 = StartPending / 3 = StopPending  / 4 = Running / 5 = Uknown

from subprocess import run as subRun
from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW
from json import loads as jsLoads
from json import JSONDecodeError

class WinService:   
    def check_state_single_host_service(hostName:str, service:str) -> list :
        out = {}
        si = STARTUPINFO()                      # startupinfo
        si.dwFlags |= STARTF_USESHOWWINDOW      # to hide powershell window
        
        powershellString = f"Get-Service -ComputerName '{hostName}' -Name '{service}' -ErrorAction Ignore | Select-Object Name, Status | ConvertTo-Json" # PS Sting
        process = subRun(['powershell', powershellString], capture_output=True, startupinfo=si)     # start powershell with powershellstring, capture_output = True == get console out
        try:
            out[hostName] = jsLoads(process.stdout) # load console out as json in out dict
        except JSONDecodeError:
            return [[hostName, service, 5]] # Error State
        outlist = [[host, state['Name'], state['Status']] for host,state in out.items()]
        return outlist
    
    def start_service_single_host(hostName:str, serviceName:str) -> bool:
        si = STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        
        subRun(['powershell',f"Get-Service -ComputerName '{hostName}' -Name '{serviceName}' | Start-Service"],startupinfo=si)
        return True
    
    def stop_service_single_host(hostName:str, serviceName:str) -> bool:
        si = STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        subRun(['powershell',f"Get-Service -ComputerName '{hostName}' -Name '{serviceName}' | Stop-Service"],startupinfo=si)
        return True

if __name__ == '__main__':
    pass