import requests
from time import sleep
from core import ServerMonitorCore

url = 'http://127.0.0.1:8000/api/servers/'
Token = '5e602c08d54111e44bfe77422296b6dc094daed3'
server_id = 9


headers = {
    "Authorization":f"Token {Token}",
    "Content-Type": "application/json"
}


def PayloadSender(server_id):
    cpu = ServerMonitorCore.cpu()
    ram = ServerMonitorCore.memory()
    disk = ServerMonitorCore.disk()
    uptime = ServerMonitorCore.UpTime_Windows()


    payload = {
        "server":server_id,
        "cpu_usage":int(cpu.get_cpu_percent()),
        "ram_usage":int((ram.get_memory().used/ram.get_memory().total)*100),
        "disk_usage":int((disk.get_disk_usage('C://').used/disk.get_disk_usage('C://').total)*100),
        # "uptime":uptime
    }
    return payload


while True: 
    data = PayloadSender(server_id)
    request = requests.put(url, json=data, headers=headers)
    print(request.status_code, request.text)
    sleep(10)

