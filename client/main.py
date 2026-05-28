from core import ServerMonitorCore
import requests
from time import sleep
import json


url = 'http://127.0.0.1:8000/monitoringdata/'

def json_convertor(data):
    return json.dumps(data, indent=len(data))


def SendData():
    cpu = ServerMonitorCore.cpu()
    ram = ServerMonitorCore.memory()
    disk = ServerMonitorCore.disk()
    uptime = ServerMonitorCore.UpTime_Windows()
    obj = {
        "cpu_usage":cpu.get_cpu_percent(),
        "ram_usage":ram.get_memory().used,
        "disk_usage":disk.get_disk_usage('C://').used,
        "uptime":uptime
    }
    return obj
json_convertor(SendData())