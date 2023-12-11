# Service = State 1 = stopped / 2 = StartPending / 3 = StopPending  / 4 = Running / 5 = Uknown

from subprocess import run as subRun
from json import loads as jsLoads
from json import JSONDecodeError

class WinService:
    def check_state_single_host(hostName:str, services:list) -> list:
        out = {}
        outlist = []
        powershellString = f"Get-Service -ComputerName '{hostName}' -Name '{",".join(services)}' -ErrorAction Ignore | Select-Object Name, Status | ConvertTo-Json"
        process = subRun(['powershell', powershellString], capture_output=True) 
        try:
            out[hostName] = jsLoads(process.stdout)
        except JSONDecodeError:
            return [[hostName, services[0], 5]]
        for host, serivce in out.items():
            if type(serivce) == list:
                for name, status in serivce:
                    outlist.append([host,name,status])
            else:
                outlist.append([host,serivce['Name'],serivce['Status']])
                
        return outlist
    
    def start_service_single_host(hostName:str, serviceName:str) -> bool:
        subRun(['powershell',f"Get-Service -ComputerName '{hostName}' -Name '{serviceName}' | Start-Service"])
        return True
    
    def stop_service_single_host(hostName:str, serviceName:str) -> bool:
        subRun(['powershell',f"Get-Service -ComputerName '{hostName}' -Name '{serviceName}' | Stop-Service"])
        return True

if __name__ == '__main__':
    pass
