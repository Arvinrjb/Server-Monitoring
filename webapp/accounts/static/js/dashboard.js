const serverSelect = document.getElementById("serverSelect");
const serversAPI = "http://127.0.0.1:8000/api/servers/";
const API_ALERTS = 'http://127.0.0.1:8000/api/alerts/';

let cachedData = [];
let performanceChart = null;

async function loadAlerts() {
    try {
        const response = await fetch(API_ALERTS);
        const data = await response.json();
        const alerts = data.results || data; 
        if (alerts.length > 0) {
            showAlerts(alerts);
        }
    } catch (error) {
        console.error("Error fetching alerts:", error);
    }
}

function showAlerts(alerts) {
    const container = document.getElementById('alertsContainer');
    container.innerHTML = '';
    alerts.forEach(alert => {
        if (alert.is_active){
            const alertEl = document.createElement('div');
            alertEl.className = `alert-item ${alert.level}`;
            alertEl.innerHTML = `
                <span class="alert-icon">⚠️</span>
                <div class="alert-content">
                    <div class="alert-title">${alert.title}</div>
                    <div class="alert-server">Server: ${alert.server_name}</div>
                    <div class="alert-message">${alert.message}</div>
                </div>
                <button class="close-alert" onclick="this.parentElement.remove()">×</button>
            `;
            container.appendChild(alertEl);
        }
    });
}

async function loadData() {
    try {
        const response = await fetch(serversAPI, { credentials: "include" });
        cachedData = await response.json();
        const serverList = cachedData.results || cachedData;
        setupServers(serverList);
        if (serverList.length > 0) {
            updateUI(serverList[0]);
        }
    } catch (err) {
        console.error("API Error:", err);
    }
}

function setupServers(data) {
    serverSelect.innerHTML = "";
    data.forEach((server, index) => {
        const option = document.createElement("option");
        option.value = index; 
        option.textContent = `${server.hostname} (${server.ipaddress})`;
        serverSelect.appendChild(option);
    });
}

function updateUI(item) {
    if (!item) return;
    const server = item.latest_status;
    const statusEl = document.querySelector(".status");
    
    if (item.status === "online"){
        statusEl.innerText = "online";
        statusEl.style.color = "#22c55e"; 
    } else {
        statusEl.innerText = "offline";
        statusEl.style.color = "#ef4444";
    }

    if (server) {
        document.querySelector(".cpu-progress").style.width = server.cpu_usage + "%";
        document.querySelector(".ram-progress").style.width = server.ram_usage + "%";
        document.querySelector(".disk-progress").style.width = server.disk_usage + "%";
        document.querySelector(".network-progress").style.width = (server.network_in ? Math.min(server.network_in, 100) : 0) + "%";

        document.querySelector(".cards .card:nth-child(1) p").innerText = server.cpu_usage + "%";
        document.querySelector(".cards .card:nth-child(2) p").innerText = server.ram_usage + "%";
        document.querySelector(".cards .card:nth-child(3) p").innerText = server.disk_usage + "%";
        document.querySelector(".cards .card:nth-child(4) p").innerText = server.network_in + " Mbps";
        document.querySelector(".info-box:nth-child(3) p").innerText = server.uptime || "-";
        document.querySelector(".info-box:nth-child(4) p").innerText = server.processes || "-";
    }

    document.querySelector(".server-header h2").innerText = item.hostname;
    document.querySelector(".info-box:nth-child(1) p").innerText = item.ipaddress;
    document.querySelector(".info-box:nth-child(2) p").innerText = item.os;
}

function showDashboardPage() {
    document.getElementById('metricsPage').style.display = 'none';
    document.getElementById('dashboardView').style.display = 'block';
    document.querySelectorAll('.menu a').forEach(a => a.classList.remove('active'));
    document.getElementById('dashboardMenuBtn').classList.add('active');
}

function showMetricsPage() {
    document.getElementById('dashboardView').style.display = 'none';
    document.getElementById('metricsPage').style.display = 'block';
    document.querySelectorAll('.menu a').forEach(a => a.classList.remove('active'));
    document.getElementById('metricsMenuBtn').classList.add('active');
    generateServerSelector();
}

async function generateServerSelector() {
    const container = document.getElementById('serverSelectorContainer');
    container.innerHTML = '<p style="color: #94a3b8;">Loading servers...</p>';
    try {
        const res = await fetch(serversAPI);
        const servers = await res.json();
        const serverList = servers.results || servers;
        container.innerHTML = '';
        
        serverList.forEach((server, index) => {
            const btn = document.createElement('button');
            btn.textContent = server.hostname;
            btn.className = 'view-btn';
            btn.onclick = () => {
                document.querySelectorAll('#serverSelectorContainer .view-btn').forEach(b => {
                    b.style.background = '#1e293b';
                    b.style.color = '#cbd5e1';
                });
                btn.style.background = '#0ea5e9'; 
                btn.style.color = '#ffffff';
                loadChartData(server.id);
            };
            container.appendChild(btn);
            if (index === 0) btn.click();
        });
    } catch (error) {
        console.error("Error generating server selector:", error);
    }
}

async function loadChartData(serverId) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/servers/${serverId}/chart/`);
        const data = await res.json();
        const labels = data.map(item => item.time);
        const cpuData = data.map(item => item.cpu);
        const ramData = data.map(item => item.ram);
        const diskData = data.map(item => item.disk);
        const ctx = document.getElementById('metricsChart').getContext('2d');
        
        if (performanceChart) {
            performanceChart.destroy();
        }
        
        performanceChart = new Chart(ctx, {
            type: 'line', 
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'CPU Usage (%)',
                        data: cpuData,
                        borderColor: '#f59e0b', 
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        tension: 0.3 
                    },
                    {
                        label: 'RAM Usage (%)',
                        data: ramData,
                        borderColor: '#10b981', 
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: 'Disk Usage (%)',
                        data: diskData,
                        borderColor: '#0ea5e9',
                        backgroundColor: 'rgba(14, 165, 233, 0.1)',
                        borderWidth: 2,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#e2e8f0' } }
                },
                scales: {
                    x: {
                        grid: { color: '#334155' }, 
                        ticks: { color: '#94a3b8' }
                    },
                    y: {
                        min: 0,
                        max: 100, 
                        grid: { color: '#334155' },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    } catch (error) {
        console.error("Error loading chart data:", error);
    }
}

serverSelect.addEventListener("change", (e) => {
    const index = e.target.value;
    const serverList = cachedData.results || cachedData;
    updateUI(serverList[index]);
});

document.addEventListener('DOMContentLoaded', () => {
    loadAlerts();
    loadData();
    if (window.location.hash === '#metricsPage') {
        showMetricsPage();
    }
});