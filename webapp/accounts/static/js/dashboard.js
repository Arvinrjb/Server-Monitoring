const serverSelect = document.getElementById("serverSelect");

const serversAPI = "http://127.0.0.1:8000/api/servers/";

// اینجا کل دیتا ذخیره میشه
let cachedData = [];

// گرفتن دیتا فقط یک بار
async function loadData() {
    try {
        const response = await fetch(serversAPI, {
            credentials: "include"
        });

        cachedData = await response.json();

        setupServers(cachedData);

        // انتخاب اولین سرور
        if (cachedData.length > 0) {
            updateUI(cachedData[0]);
        }

    } catch (err) {
        console.error("API Error:", err);
    }
}

// پر کردن dropdown
function setupServers(data) {
    serverSelect.innerHTML = "";

    data.forEach((item, index) => {
        const server = item.server;

        const option = document.createElement("option");
        option.value = index; // مهم: index نگه می‌داریم
        option.textContent = `${server.hostname} (${server.ipaddress})`;

        serverSelect.appendChild(option);
    });
}

// آپدیت UI بدون API
function updateUI(item) {

    const server = item.server;

    // progress bars
    document.querySelector(".cpu-progress").style.width = item.cpu_usage + "%";
    document.querySelector(".ram-progress").style.width = item.ram_usage + "%";
    document.querySelector(".disk-progress").style.width = item.disk_usage + "%";

    // text values
    document.querySelector(".cards .card:nth-child(1) p").innerText = item.cpu_usage + "%";
    document.querySelector(".cards .card:nth-child(2) p").innerText = item.ram_usage + "%";
    document.querySelector(".cards .card:nth-child(3) p").innerText = item.disk_usage + "%";

    // server info
    document.querySelector(".server-header h2").innerText = server.hostname;

    document.querySelector(".info-box:nth-child(1) p").innerText = server.ipaddress;
    document.querySelector(".info-box:nth-child(2) p").innerText = server.os;

    document.querySelector(".info-box:nth-child(3) p").innerText = item.uptime;
}

// وقتی کاربر سرور را تغییر می‌دهد
serverSelect.addEventListener("change", (e) => {
    const index = e.target.value;
    updateUI(cachedData[index]);
});

// شروع
loadData();