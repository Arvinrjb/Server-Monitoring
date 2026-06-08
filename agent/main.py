import requests
from time import sleep
from core import ServerMonitorCore
import datetime

token_url = ''
url = 'http://127.0.0.1:8000/api/agent/report/'
Token = 'a21f3f3ee4fb31e75c5c59176783f178aa5b4ac5e81b24301fc99219cb2cb875'
headers = {
    "X-Agent-Token":Token,
    "Content-Type": "application/json"
}



def Get_Token(token_url):
    return requests.get(token_url)


def PayloadSender(time, date):
    cpu = ServerMonitorCore.cpu()
    ram = ServerMonitorCore.memory()
    disk = ServerMonitorCore.disk()
    uptime = ServerMonitorCore.UpTime_Windows()



    payload = {
        "cpu_usage":int(cpu.get_cpu_percent()),
        "ram_usage":int((ram.get_memory().used/ram.get_memory().total)*100),
        "disk_usage":int((disk.get_disk_usage('C://').used/disk.get_disk_usage('C://').total)*100),
        "lastupdate":f"{date}T{time}Z"
    }
    return payload


while True: 
    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()
    data = PayloadSender(time, date)
    # print(data)
    request = requests.post(url, json=data, headers=headers)
    print(request.status_code, request.text)
    sleep(10)



