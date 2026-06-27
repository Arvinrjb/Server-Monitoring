import psutil
import os
import ctypes

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
    

    

def UpTime_Linux():
    return os.popen('uptime -p').read()[:-1]


def UpTime_Windows():
    lib = ctypes.windll.kernel32
    time = lib.GetTickCount64()
    time = int(str(time)[:-3])
    return time


if __name__ == "__main__":
    pass


