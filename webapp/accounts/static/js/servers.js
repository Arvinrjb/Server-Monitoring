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

const serverModal = document.getElementById("serverModal");
const addServerBtn = document.getElementById("addServerBtn");
const serverContainer = document.getElementById("serverContainer");

addServerBtn.addEventListener("click", () => {
    serverModal.style.display = "flex";
});

window.addEventListener("click", (e) => {
    if (e.target === serverModal) {
        serverModal.style.display = "none";
    }
});

async function loadServers() {
    try {
        const response = await fetch("/api/addserver/");
        const data = await response.json();
        
        serverContainer.innerHTML = "";

        const servers = data.results || data;

        servers.forEach(server => {
            serverContainer.innerHTML += `
                <div class="server-row">
                    <span>${server.hostname}</span>
                    <span>${server.ipaddress}</span>
                    <span class="${server.status}">${server.status}</span>
                    <div class="actions">
                        <button class="view-btn" onclick="showLogs(${server.id}, '${server.hostname}')">
                            ViewLogs
                        </button>
                        <button class="delete-btn" onclick="deleteServer(${server.id})">
                            Delete
                        </button>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error loading servers:", error);
    }
}

async function deleteServer(id) {
    if (!confirm("Are you sure you want to delete this server?")) return;

    const csrftoken = getCookie('csrftoken');
    
    await fetch(`/api/addserver/${id}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": csrftoken
        }
    });
    
    loadServers();
}

document.getElementById("serverForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const csrftoken = getCookie('csrftoken');
    
    const hostname = document.getElementById("hostname").value;
    const ipaddress = document.getElementById("ipaddress").value;
    const os = document.getElementById("os").value;

    await fetch("/api/addserver/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            hostname,
            ipaddress,
            os
        })
    });

    serverModal.style.display = "none";
    document.getElementById("serverForm").reset();
    loadServers();
});


const API_LOG = 'http://127.0.0.1:8000/api';

function showLogs(serverId, hostname) {
    const modal = document.getElementById('logsModal');
    const container = document.getElementById('logsContainer');
    const title = document.getElementById('logsServerName');

    title.textContent = `Recent Logs - ${hostname}`;
    modal.style.display = 'flex';
    container.innerHTML = '<p style="text-align:center; padding:40px; color:#64748b;">Loading logs....</p>';

    fetch(`${API_LOG}/logs/?server=${serverId}&limit=20`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch logs');
            return response.json();
        })
        .then(data => {
            container.innerHTML = '';
            const logs = data.results || data;

            if (!Array.isArray(logs) || logs.length === 0) {
                container.innerHTML = '<p style="text-align:center; color:#94a3b8; padding:40px;">No logs found.</p>';
                return;
            }

            logs.forEach(log => {
                const level = (log.level || 'INFO').toLowerCase();
                const logItem = document.createElement('div');
                logItem.className = `log-item ${level}`;
                logItem.innerHTML = `
                    <div class="log-time">${new Date(log.created_at).toLocaleString('en-US')}</div>
                    <div class="log-message">
                        <strong>[${log.level || 'INFO'}]</strong> ${log.message}
                    </div>
                `;
                container.appendChild(logItem);
            });
        })
        .catch(err => {
            console.error(err);
            container.innerHTML = `
                <p style="color:#ef4444; text-align:center; padding:40px;">
                   Error retrieving logs<br>
                    <small>${err.message}</small>
                </p>`;
        });
}

function closeLogsModal() {
    document.getElementById('logsModal').style.display = 'none';
}

document.getElementById('logsModal').addEventListener('click', function(e) {
    if (e.target === this) closeLogsModal();
});

document.addEventListener('DOMContentLoaded', () => {
    loadServers();
});