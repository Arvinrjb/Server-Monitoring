import requests
import datetime
from time import sleep
from core import ServerMonitorCore
from core.logger import logging

def status_sender(url, token):
    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()
    cpu = ServerMonitorCore.cpu()
    ram = ServerMonitorCore.memory()
    disk = ServerMonitorCore.disk()
    network = ServerMonitorCore.network()
    old_speed = network.get_net_io_counters()
    sleep(1)
    new_speed = network.get_net_io_counters()
    download_speed = ((new_speed.bytes_recv-old_speed.bytes_recv)/1024 /1024) * 8
    # download_speed = ((new_speed.bytes_recv-old_speed.bytes_recv)/1024 /1024)*8)/10 

    if int(cpu.get_cpu_percent()) >= 90:
        logging.warning("CPU usage is greater than 90.")

    if int((ram.get_memory().used/ram.get_memory().total)*100) >= 90:
        logging.warning("RAM usage is greater than 90.")

    if int((disk.get_disk_usage('C://').used/disk.get_disk_usage('C://').total)*100) >= 90 :
        logging.warning("DISK usage is greater than 90.")

    headers = {
    "X-Agent-Token":token,
    "Content-Type": "application/json"
    }
    payload = {
        "cpu_usage":int(cpu.get_cpu_percent()),
        "ram_usage":int((ram.get_memory().used/ram.get_memory().total)*100),
        "disk_usage":int((disk.get_disk_usage('C://').used/disk.get_disk_usage('C://').total)*100),
        "network_in":int(download_speed),
        "lastupdate":f"{date}T{time}Z",
    }
    request = requests.post(url, json=payload, headers=headers)
    return request




