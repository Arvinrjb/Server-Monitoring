use sysinfo::{
    System, Disks
};

pub struct Cpu {
    cpu_percent: f32,
    process_count: usize,
}


pub struct Ram {
    memory_used:u64,
    swap_used:u64
}

pub struct Disk{
    disk_name:String,
    disk_availbale_space:u64
}

impl Cpu {
    pub fn new() -> Self{
        let mut system = match System::new_all(){
            Ok(system) => system,
            Err(err) => panic!("Error {err}")
        };
        
        std::thread::sleep(sysinfo::MINIMUM_CPU_UPDATE_INTERVAL);
        system.refresh_cpu_all();
        let proc = system.processes();
        Self{
            cpu_percent: system.global_cpu_usage(),
            process_count: proc.len()
        }
    }

    pub fn get_cpu_percent(&self) ->f32 {
        self.cpu_percent
    }

    pub fn get_processes(&self) -> usize{
        self.process_count
    }



}


impl Ram {
    pub fn new() -> Self{
        let mut system = match System::new_all() {
            Ok(system) => system,
            Err(err) => panic!("Error {err}")
        };
        system.refresh_all();
        Self{
            memory_used:system.used_memory()/1073741824,
            swap_used:system.used_swap()/1073741824
        }
    }

    pub fn get_memory(&self) -> u64 {
        self.memory_used
    }

    pub fn get_swap_memory(&self) -> u64{
        self.swap_used
    }
}


impl Disk {
    pub fn new() -> Self{
        let disk = match Disks::new_with_refreshed_list() {
            Ok(disk) => disk,
            Err(err) => panic!("{err}")
        };
        
        Self{
            disk_name:disk[0].name().to_string_lossy().into_owned(),
            disk_availbale_space:disk[0].available_space()/1073741824
        }
        
    }

    pub fn get_disk_usage(&self) -> u64{
        self.disk_availbale_space
    }

    pub fn get_disk_name (&self) -> String{
        self.disk_name.clone()
    }

}