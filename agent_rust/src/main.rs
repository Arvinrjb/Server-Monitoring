// Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
// See the LICENSE file in the project root for the full license text.
// Copyright (C) 2026 arvin, arvinrjb13@gmail.com

mod monitoring_core;
use monitoring_core::{
    Cpu, Disk, Ram, Network, get_uptime, get_lastupdate
};


fn main() {
    let token = String::from("105958cf9e5d3f498eb18cf3c4ab9f5bda23c6b0ea096ea4fd5c6232e2d69761");
    let status_url = String::from("http://127.0.0.1:8000/api/agent/status/report/");
    status_sender(&status_url, &token);
}


fn status_sender(url:&str, token:&str){
    let client = reqwest::blocking::Client::new();
    let disk = Disk::new();
    let cpu = Cpu::new();
    let ram = Ram::new();
    let network = Network::new();

    let payload = serde_json::json!({
        "uptime_seconds": get_uptime(),
        "process_count": cpu.get_processes(),
        "cpu_usage": cpu.get_cpu_percent(),
        "ram_usage": ram.get_memory(),
        "disk_usage": disk.get_disk_usage(),
        "network_in": network.get_downlaod_speed(),
        "network_out": network.get_upload_speed(),
        "lastupdate": get_lastupdate()
    });

    let response = client
        .post(url)
        .header("X-Agent-Token", token)
        .json(&payload)
        .send().expect("error")
        .error_for_status();

    println!("API status: {}", 201);
    
}