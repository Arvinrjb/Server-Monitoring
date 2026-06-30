const serverContainer = document.getElementById("serverContainer");
const serverModal = document.getElementById("serverModal");
const editServerModal = document.getElementById("editServerModal"); // جدید
const addServerBtn = document.getElementById("addServerBtn");
const serverForm = document.getElementById("serverForm");
const editServerForm = document.getElementById("editServerForm"); // جدید
const logsModal = document.getElementById("logsModal");
const logsContainer = document.getElementById("logsContainer");
const logsServerName = document.getElementById("logsServerName");

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

async function loadServers() {
    try {
        const response = await fetch("/api/addserver/");
        const data = await response.json();
        const servers = data.results || data;
        
        serverContainer.innerHTML = "";
        if (!servers || servers.length === 0) {
            serverContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: #64748b;">No servers found.</div>';
            return;
        }

        servers.forEach(server => {
            const statusClass = (server.status || "offline").toLowerCase();
            serverContainer.innerHTML += `
                <div class="server-row">
                    <span style="font-weight: 600;">${server.hostname}</span>
                    <span>${server.ipaddress}</span>
                    <span class="${statusClass}">${server.status}</span>
                    <div class="actions">
                        <button class="edit-btn" onclick="openEditModal(${server.id}, '${server.hostname}', '${server.os}', '${server.status}')">Edit</button>
                        <button class="view-btn" onclick="showLogs(${server.id}, '${server.hostname}')">Logs</button>
                        <button class="delete-btn" onclick="deleteServer(${server.id})">Delete</button>
                    </div>
                </div>
            `;
        });
    } catch (error) { console.error("Error loading servers:", error); }
}

serverForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const csrftoken = getCookie('csrftoken');
    const payload = {
        hostname: document.getElementById("hostname").value,
        ipaddress: document.getElementById("ipaddress").value,
        os: document.getElementById("os").value
    };

    const response = await fetch("/api/addserver/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        serverModal.style.display = "none";
        serverForm.reset();
        loadServers();
    }
});

function openEditModal(id, hostname, os, status) {
    document.getElementById('editServerId').value = id;
    document.getElementById('editHostname').value = hostname;
    document.getElementById('editOs').value = os;
    document.getElementById('editStatus').value = status;
    editServerModal.style.display = 'flex';
}

editServerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById('editServerId').value;
    const csrftoken = getCookie('csrftoken');
    const payload = {
        hostname: document.getElementById("editHostname").value,
        os: document.getElementById("editOs").value,
        status: document.getElementById("editStatus").value
    };

    const response = await fetch(`/api/addserver/${id}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        editServerModal.style.display = 'none';
        loadServers();
    }
});

async function deleteServer(id) {
    if (!confirm("Are you sure?")) return;
    await fetch(`/api/addserver/${id}/`, { method: "DELETE", headers: { "X-CSRFToken": getCookie('csrftoken') } });
    loadServers();
}

function showLogs(serverId, hostname) {
    logsServerName.textContent = `Recent Logs - ${hostname}`;
    logsModal.style.display = 'flex';
    logsContainer.innerHTML = '<p style="padding:20px;">Loading...</p>';

    fetch(`http://127.0.0.1:8000/api/logs/?server=${serverId}`)
        .then(res => res.json())
        .then(data => {
            logsContainer.innerHTML = '';
            (data.results || data).forEach(log => {
                logsContainer.innerHTML += `<div class="log-item ${(log.level || 'info').toLowerCase()}">
                    <div class="log-message">${log.message}</div></div>`;
            });
        });
}

addServerBtn.addEventListener("click", () => serverModal.style.display = "flex");

window.addEventListener("click", (e) => {
    if (e.target === serverModal) serverModal.style.display = "none";
    if (e.target === editServerModal) editServerModal.style.display = "none";
    if (e.target === logsModal) logsModal.style.display = "none";
});

document.addEventListener("DOMContentLoaded", loadServers);
