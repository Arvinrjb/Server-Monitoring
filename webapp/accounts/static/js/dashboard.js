const serverSelect = document.getElementById("serverSelect");

const serversAPI = "http://127.0.0.1:8000/api/servers/";


let cachedData = [];


async function loadData() {
    try {
        const response = await fetch(serversAPI, {
            credentials: "include"
        });

        cachedData = await response.json();

        setupServers(cachedData.results);
        if (cachedData.results.length > 0) {
            updateUI(cachedData.results[0]);
        }

    } catch (err) {
        console.error("API Error:", err);
    }
}

function setupServers(data) {
    serverSelect.innerHTML = "";

    data.forEach((item, index) => {
        const server = item

        const option = document.createElement("option");
        option.value = index; 
        option.textContent = `${server.hostname} (${server.ipaddress})`;

        serverSelect.appendChild(option);
    });
}

function updateUI(item) {
    const server = item.latest_status;
    if (item.status == "online"){
        document.querySelector(".status").innerText = "online" 
        document.querySelector(".status").style.color = "#30d30f" 
    }else{
       document.querySelector(".status").innerText = "offline"
       document.querySelector(".status").style.color = "#ed3232"
    }
    document.querySelector(".cpu-progress").style.width = server.cpu_usage + "%";
    document.querySelector(".ram-progress").style.width = server.ram_usage + "%";
    document.querySelector(".disk-progress").style.width = server.disk_usage + "%";
    document.querySelector(".network-progress").style.width = server.network_in + "%";

    document.querySelector(".cards .card:nth-child(1) p").innerText = server.cpu_usage + "%";
    document.querySelector(".cards .card:nth-child(2) p").innerText = server.ram_usage + "%";
    document.querySelector(".cards .card:nth-child(3) p").innerText = server.disk_usage + "%";
    document.querySelector(".cards .card:nth-child(4) p").innerText = server.network_in + "%";

    document.querySelector(".server-header h2").innerText = item.hostname;

    document.querySelector(".info-box:nth-child(1) p").innerText = item.ipaddress;
    document.querySelector(".info-box:nth-child(2) p").innerText = item.os;

    document.querySelector(".info-box:nth-child(3) p").innerText = server.uptime;
}


serverSelect.addEventListener("change", (e) => {
    const index = e.target.value;
    updateUI(cachedData.results[index]);
});


loadData();