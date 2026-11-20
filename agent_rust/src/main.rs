// Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
// See the LICENSE file in the project root for the full license text.
// Copyright (C) 2026 arvin, arvinrjb13@gmail.com

mod monitoring_core;
use monitoring_core::{
    Cpu, Disk, Ram, Network, get_uptime
};


fn main() {
    let disk = Disk::new();
    let cpu = Cpu::new();
    let ram = Ram::new();
    let network = Network::new();

    println!("uptime: {}h", get_uptime()/3600);
    println!("network_in: {}MB, network_out: {}MB", network.get_network_in()/1048576, network.get_network_out()/1048576);
    println!("used memory: {}GB swap used: {}GB", ram.get_memory()/1073741824, ram.get_swap_memory()/1073741824);
    println!("{} : {}GB", disk.get_disk_name(), disk.get_disk_usage()/1073741824); 
    println!("cpu :{:0.2}, processes: {}", cpu.get_cpu_percent(), cpu.get_processes())    
}
