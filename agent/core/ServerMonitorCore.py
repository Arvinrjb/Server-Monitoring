# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

import psutil
import time


class cpu:
    def get_cpu_time(self):
        return psutil.cpu_times(percpu=False)

    def get_cpu_percent(self):
        return psutil.cpu_percent(interval=1, percpu=False)
    

    def get_cpu_count(self):
        self.logicalCore = psutil.cpu_count()
        self.physicalCore = psutil.cpu_count(logical=False)
        return self.physicalCore, self.logicalCore
    
    def get_cpu_frequency(self):
        return psutil.cpu_freq()
    
    def get_cpu_loadavg(self):
        return psutil.getloadavg()
    
    def get_process_count(self):
        return sum(1 for _ in psutil.process_iter())


class memory:
    def get_memory(self):
        return psutil.virtual_memory()
    
    def get_swap_memory(self):
        return psutil.swap_memory()
    

class disk:
    def get_disk_partitions(self):
        return psutil.disk_partitions(all=True)
    
    def get_disk_usage(self, disk_path):
        return psutil.disk_usage(disk_path)

    def get_disk_io_counters(self):
        return psutil.disk_io_counters(perdisk=True)


class network:
    def get_net_io_counters(self):
        return psutil.net_io_counters(pernic=False)
    

    

def get_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    return uptime_seconds


if __name__ == "__main__":
    pass


