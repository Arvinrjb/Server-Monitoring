// Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
// See the LICENSE file in the project root for the full license text.
// Copyright (C) 2026 arvin, arvinrjb13@gmail.com

use sysinfo::{
    System, Disks, Networks
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

pub struct Network{
    network_in: u64,
    network_out: u64
} 

pub fn get_uptime() -> u64{
    let up_time = match System::uptime(){
        Ok(uptime) => uptime,
        Err(err) => panic!("Failed to get `uptime`: {err}")
    };
    up_time
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
            memory_used:system.used_memory(),
            swap_used:system.used_swap()
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
            disk_availbale_space:disk[0].available_space()
        }
        
    }

    pub fn get_disk_usage(&self) -> u64{
        self.disk_availbale_space
    }

    pub fn get_disk_name (&self) -> String{
        self.disk_name.clone()
    }

}


impl Network {
    pub fn new() -> Self {
        let network = match Networks::new_with_refreshed_list() {
            Ok(netwok) => netwok,
            Err(err) => panic!("{err}")
        };
        let interface_name = String::from("eno1");
        for (interface, network) in &network{
            if interface.to_string_lossy() == interface_name{    
                return Self {
                    network_in: network.total_received(),
                    network_out: network.total_transmitted()
                };
            };
        };
        return Self { network_in: 0, network_out: 0 };
    }

    pub fn get_network_in(&self) -> u64 {
        self.network_in
    }

    pub fn get_network_out(&self) -> u64 {
        self.network_out
    }
}