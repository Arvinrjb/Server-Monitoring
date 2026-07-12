# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

import requests
import datetime
from time import sleep
from core import ServerMonitorCore
from core.logger import logger

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
    upload_speed = ((new_speed.bytes_sent-old_speed.bytes_sent)/1024 /1024) * 8

    if int(cpu.get_cpu_percent()) >= 90:
        logger.warning("CPU usage is greater than 90.")

    if int((ram.get_memory().used/ram.get_memory().total)*100) >= 90:
        logger.warning("RAM usage is greater than 90.")

    if int((disk.get_disk_usage('/').used/disk.get_disk_usage('/').total)*100) >= 90 :
        logger.warning("DISK usage is greater than 90.")

    headers = {
    "X-Agent-Token":token,
    "Content-Type": "application/json"
    }
    payload = {
        "uptime_seconds":ServerMonitorCore.get_uptime(),
        "process_count":cpu.get_process_count(),
        "cpu_usage":int(cpu.get_cpu_percent()),
        "ram_usage":int((ram.get_memory().used/ram.get_memory().total)*100),
        "disk_usage":int((disk.get_disk_usage('/').used/disk.get_disk_usage('/').total)*100),
        "network_in":int(download_speed),
        "network_out":int(upload_speed),
        "lastupdate":f"{date}T{time}Z",
    }
    request = requests.post(url, json=payload, headers=headers)
    return request




