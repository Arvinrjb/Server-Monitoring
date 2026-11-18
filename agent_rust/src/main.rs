mod monitoring_core;
use monitoring_core::{Cpu, Disk, Ram};



fn main() {
    let disk = Disk::new();
    let cpu = Cpu::new();
    let ram = Ram::new();
    println!("used memory: {} swap used: {}", ram.get_memory(), ram.get_swap_memory());
    println!("{} : {}GB", disk.get_disk_name(), disk.get_disk_usage()); 
    println!("cpu :{:0.2}, processes: {}", cpu.get_cpu_percent(), cpu.get_processes())    
    }
