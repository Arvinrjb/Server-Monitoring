const API_SERVERS = 'http://127.0.0.1:8000/api/servers/';
const API_LOGS = 'http://127.0.0.1:8000/api/logs/';
const API_ALERTS = 'http://127.0.0.1:8000/api/alerts/';

let currentServerId = null;

async function loadServers() {
    try {
        const res = await fetch(API_SERVERS);
        const data = await res.json();
        const servers = data.results || data;

        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        servers.forEach(server => { 
            const hasAlert = server.lastes_alert?.is_active === true;

            const cpu = server.latest_status?.cpu_usage || 0;
            const ram = server.latest_status?.ram_usage || 0;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${server.hostname}</td>
                <td>${server.ipaddress}</td>
                <td>${server.user?.username || server.user || 'N/A'}</td>
                <td><span class="${server.status || 'offline'}">${server.status || 'offline'}</span></td>
                <td>
                    <div class="usage-bar">
                        <div class="usage-fill cpu-fill" style="width: ${cpu}%"></div>
                    </div>
                    ${cpu}%
                </td>
                <td>
                    <div class="usage-bar">
                        <div class="usage-fill ram-fill" style="width: ${ram}%"></div>
                    </div>
                    ${ram}%
                </td>
                <td>${hasAlert ? '<span class="alert-icon">⚠️</span>' : ''}</td>
                <td><button class="view-btn">Details</button></td>
            `;

            row.onclick = () => showServerDetails(server.id, server);
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading servers:", error);
    }
}

async function showServerDetails(id, server) {
    currentServerId = id;
    document.getElementById('modalServerName').textContent = server.hostname;
    document.getElementById('detailModal').style.display = 'flex';

    // Overview
    document.getElementById('overviewContent').innerHTML = `
        <p><strong>IP:</strong> ${server.ipaddress}</p>
        <p><strong>Owner:</strong> ${server.user?.username || 'N/A'}</p>
        <p><strong>OS:</strong> ${server.os || 'N/A'}</p>
        <p><strong>Status:</strong> ${server.status}</p>
    `;

    loadServerLogs(id);
    loadServerAlerts(id);
}

function closeDetailModal() {
    document.getElementById('detailModal').style.display = 'none';
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    loadServers();
});