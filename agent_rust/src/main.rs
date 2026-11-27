// Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
// See the LICENSE file in the project root for the full license text.
// Copyright (C) 2026 arvin, arvinrjb13@gmail.com

#![allow(while_true)]

mod monitoring_core;
use std::time::Duration;
use std::thread::sleep;
use flexi_logger::{
    DeferredNow, FileSpec, Logger, WriteMode,
};
use log::{error, info, warn, Record};
use monitoring_core::{
    Cpu, Disk, Ram, Network, get_uptime, get_lastupdate
};


fn main(){
    let _logger = Logger::try_with_str("info").unwrap()
        .log_to_file(FileSpec::default().basename("agent").suppress_timestamp())
        .format(agent_log_format)
        .append()
        .write_mode(WriteMode::BufferAndFlush)
        .start().unwrap();

    info!("Server Monitoring Started");

    let token = String::from("105958cf9e5d3f498eb18cf3c4ab9f5bda23c6b0ea096ea4fd5c6232e2d69761");
    let status_url = String::from("http://127.0.0.1:8000/api/agent/status/report/");    
    
    while true {
        match status_sender(&status_url, &token){
            Ok(status) => {
                if status.is_success(){
                    println!("API status: {status}");
                    sleep(Duration::from_secs(5));
                }else {
                    warn!("Status API returned HTTP {status}");
                    sleep(Duration::from_secs(10));
                }
            },
            Err(error) =>  {
                sleep(Duration::from_secs(10));
                eprintln!("{error}");
                error!("Failed to send status: {error}");
            }
        }
    }
}

fn agent_log_format(
    w: &mut dyn std::io::Write,
    now: &mut DeferredNow,
    record: &Record,
) -> std::io::Result<()> {
    write!(
        w,
        "{} | {} | {}",
        now.format("%Y-%m-%d %H:%M:%S"),
        record.level(),
        record.args()
    )
}


fn status_sender(url:&str, token:&str) -> Result<reqwest::StatusCode, reqwest::Error>{
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

    if *&payload["cpu_usage"].as_i64().unwrap() >= 90{
        warn!("CPU usage is greater than 90.");
    }
    if *&payload["ram_usage"].as_i64().unwrap() >= 90{
        warn!("RAM usage is greater than 90.");
    }
    if *&payload["disk_usage"].as_i64().unwrap() >= 90{
        warn!("DISK usage is greater than 90.")
    }

    let response = client
        .post(url)
        .header("X-Agent-Token", token)
        .json(&payload)
        .send()?;

    
    let status = response.status();
    Ok(status)    
}
