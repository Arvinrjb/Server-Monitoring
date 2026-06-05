const serverSelect = document.getElementById("serverSelect");

const serversAPI = "http://127.0.0.1:8000/api/servers/";


let cachedData = [];


async function loadData() {
    try {
        const response = await fetch(serversAPI, {
            credentials: "include"
        });

        cachedData = await response.json();

        setupServers(cachedData);
        if (cachedData.length > 0) {
            updateUI(cachedData[0]);
        }

    } catch (err) {
        console.error("API Error:", err);
    }
}

function setupServers(data) {
    serverSelect.innerHTML = "";

    data.forEach((item, index) => {
        const server = item.server;

        const option = document.createElement("option");
        option.value = index; 
        option.textContent = `${server.hostname} (${server.ipaddress})`;

        serverSelect.appendChild(option);
    });
}

function updateUI(item) {

    const server = item.server;


    document.querySelector(".cpu-progress").style.width = item.cpu_usage + "%";
    document.querySelector(".ram-progress").style.width = item.ram_usage + "%";
    document.querySelector(".disk-progress").style.width = item.disk_usage + "%";

    document.querySelector(".cards .card:nth-child(1) p").innerText = item.cpu_usage + "%";
    document.querySelector(".cards .card:nth-child(2) p").innerText = item.ram_usage + "%";
    document.querySelector(".cards .card:nth-child(3) p").innerText = item.disk_usage + "%";

    document.querySelector(".server-header h2").innerText = server.hostname;

    document.querySelector(".info-box:nth-child(1) p").innerText = server.ipaddress;
    document.querySelector(".info-box:nth-child(2) p").innerText = server.os;

    document.querySelector(".info-box:nth-child(3) p").innerText = item.uptime;
}


serverSelect.addEventListener("change", (e) => {
    const index = e.target.value;
    updateUI(cachedData[index]);
});


loadData();