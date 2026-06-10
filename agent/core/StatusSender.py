import requests
import datetime
from core import ServerMonitorCore


def status_sender(url, token):
    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()
    cpu = ServerMonitorCore.cpu()
    ram = ServerMonitorCore.memory()
    disk = ServerMonitorCore.disk()

    headers = {
    "X-Agent-Token":token,
    "Content-Type": "application/json"
    }
    payload = {
        "cpu_usage":int(cpu.get_cpu_percent()),
        "ram_usage":int((ram.get_memory().used/ram.get_memory().total)*100),
        "disk_usage":int((disk.get_disk_usage('C://').used/disk.get_disk_usage('C://').total)*100),
        "lastupdate":f"{date}T{time}Z"
    }
    request = requests.post(url, json=payload, headers=headers)
    return request
    