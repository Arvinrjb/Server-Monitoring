import psutil


class cpu:
    def get_cpu_time(self):
        return psutil.cpu_times(percpu=False)

    def get_cpu_percent(self):
        return psutil.cpu_percent(interval=1, percpu=True)
    
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

    ## last code 


    def get_net_io_counters(self):
        return psutil.net_io_counters(pernic=True)
    




if __name__ == "__main__":
    net = network()
    print(net.get_net_io_counters())
