const API_BASE = "http://127.0.0.1:8000";

const API_SERVERS = `${API_BASE}/api/servers/`;
const API_LOGS = `${API_BASE}/api/logs/`;
const API_ALERTS = `${API_BASE}/api/alerts/`;

let currentServerId = null;
let performanceChart = null;

// ================================
// JWT Token Helpers
// ================================

function getAccessToken() {
    return localStorage.getItem("access");
}

function getRefreshToken() {
    return localStorage.getItem("refresh");
}

function setAccessToken(access) {
    localStorage.setItem("access", access);
}

function clearTokens() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
}

function redirectToLogin() {
    clearTokens();
    window.location.href = "/login/";
}

async function refreshAccessToken() {
    const refresh = getRefreshToken();

    if (!refresh) {
        return false;
    }

    try {
        const response = await fetch(`${API_BASE}/api/token/refresh/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refresh: refresh
            })
        });

        if (!response.ok) {
            return false;
        }

        const data = await response.json();

        if (!data.access) {
            return false;
        }

        setAccessToken(data.access);
        return true;
    } catch (error) {
        console.error("Token refresh error:", error);
        return false;
    }
}

async function apiFetch(url, options = {}) {
    let access = getAccessToken();

    if (!access) {
        redirectToLogin();
        throw new Error("No access token found.");
    }

    const headers = {
        ...(options.headers || {}),
        "Content-Type": "application/json",
        "Authorization": `Bearer ${access}`
    };

    let response = await fetch(url, {
        ...options,
        headers: headers
    });

    if (response.status === 401) {
        const refreshed = await refreshAccessToken();

        if (!refreshed) {
            redirectToLogin();
            throw new Error("Unauthorized.");
        }

        access = getAccessToken();

        response = await fetch(url, {
            ...options,
            headers: {
                ...(options.headers || {}),
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access}`
            }
        });
    }

    return response;
}

// ================================
// Dashboard
// ================================

async function loadServers() {
    try {
        const [serversResponse, alertsResponse] = await Promise.all([
            apiFetch(API_SERVERS),
            apiFetch(API_ALERTS)
        ]);

        const serversData = await serversResponse.json();
        const alertsData = await alertsResponse.json();

        const servers = serversData.results || serversData;
        const alerts = alertsData.results || alertsData;

        const tableBody = document.getElementById("tableBody");

        if (!tableBody) {
            return;
        }

        tableBody.innerHTML = "";

        servers.forEach(function (server) {
            const hasAlert = alerts.some(function (alert) {
                return (
                    alert.server_name &&
                    server.hostname &&
                    alert.server_name.trim().toLowerCase() === server.hostname.trim().toLowerCase() &&
                    alert.is_active === true
                );
            });

            const cpu = server.latest_status?.cpu_usage || 0;
            const ram = server.latest_status?.ram_usage || 0;

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${server.hostname}</td>
                <td>${server.ipaddress}</td>
                <td>${server.user?.username || server.user || "N/A"}</td>
                <td>
                    <span class="status-badge ${server.status || "offline"}">
                        ${server.status || "offline"}
                    </span>
                </td>
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
                <td>
                    ${hasAlert ? '<span class="alert-icon" style="color: #ef4444; font-size: 20px;">⚠</span>' : "—"}
                </td>
                <td>
                    <button class="view-btn">Details</button>
                </td>
            `;

            const detailButton = row.querySelector(".view-btn");

            detailButton.addEventListener("click", function (event) {
                event.stopPropagation();
                showServerDetails(server.id, server);
            });

            row.addEventListener("click", function () {
                showServerDetails(server.id, server);
            });

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading servers:", error);
    }
}

async function showServerDetails(serverId, server) {
    currentServerId = serverId;

    const modalName = document.getElementById("modalServerName");
    const modal = document.getElementById("detailModal");
    const overviewContent = document.getElementById("overviewContent");

    if (modalName) {
        modalName.textContent = server.hostname;
    }

    if (modal) {
        modal.classList.add("show");
    }

    openTab(0);

    if (overviewContent) {
        overviewContent.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 12px; font-size: 16px;">
                <p><strong>IP Address:</strong> ${server.ipaddress}</p>
                <p><strong>Owner:</strong> ${server.user?.username || server.user || "N/A"}</p>
                <p><strong>OS:</strong> ${server.os || "N/A"}</p>
                <p><strong>Status:</strong> ${server.status || "offline"}</p>
            </div>
        `;
    }

    await loadServerLogs(serverId);
    await loadServerAlerts(server.hostname);
}

function closeDetailModal() {
    const modal = document.getElementById("detailModal");

    if (modal) {
        modal.classList.remove("show");
    }
}

function openTab(tabIndex) {
    const contents = document.querySelectorAll(".tab-content");
    const buttons = document.querySelectorAll(".tab-btn");

    contents.forEach(function (content) {
        content.classList.remove("active");
    });

    buttons.forEach(function (button) {
        button.classList.remove("active");
    });

    const selectedContent = document.getElementById("tab" + tabIndex);

    if (selectedContent) {
        selectedContent.classList.add("active");
    }

    if (buttons[tabIndex]) {
        buttons[tabIndex].classList.add("active");
    }
}

// ================================
// Logs
// ================================

async function loadServerLogs(serverId, limit = 20) {
    const logsContent = document.getElementById("logsContent");

    if (!logsContent) {
        return;
    }

    logsContent.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="font-size: 16px; color: #38bdf8;">Server Logs</h3>

            <div>
                <label for="logLimitSelect" style="color: #94a3b8; font-size: 14px; margin-right: 8px;">
                    Show:
                </label>

                <select id="logLimitSelect" style="background: #334155; color: #fff; border: 1px solid #475569; padding: 5px 10px; border-radius: 4px;">
                    <option value="10" ${Number(limit) === 10 ? "selected" : ""}>10 Logs</option>
                    <option value="20" ${Number(limit) === 20 ? "selected" : ""}>20 Logs</option>
                    <option value="50" ${Number(limit) === 50 ? "selected" : ""}>50 Logs</option>
                    <option value="100" ${Number(limit) === 100 ? "selected" : ""}>100 Logs</option>
                </select>
            </div>
        </div>

        <div id="logsTableContainer">
            <p style="color: #94a3b8;">Loading logs...</p>
        </div>
    `;

    const limitSelect = document.getElementById("logLimitSelect");

    if (limitSelect) {
        limitSelect.addEventListener("change", function () {
            loadServerLogs(serverId, this.value);
        });
    }

    try {
        const response = await apiFetch(`${API_LOGS}?limit=${limit}&ordering=-created_at`);
        const data = await response.json();
        const allLogs = data.results || data;

        const serverLogs = allLogs.filter(function (log) {
            return String(log.server) === String(serverId);
        });

        const tableContainer = document.getElementById("logsTableContainer");

        if (!tableContainer) {
            return;
        }

        if (serverLogs.length === 0) {
            tableContainer.innerHTML = `<p style="color: #94a3b8;">No logs found for this server.</p>`;
            return;
        }

        let html = `
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px;">
                <thead>
                    <tr style="border-bottom: 2px solid #334155; color: #94a3b8;">
                        <th style="padding: 10px 5px;">Level</th>
                        <th style="padding: 10px 5px;">Message</th>
                        <th style="padding: 10px 5px; text-align: right;">Time</th>
                    </tr>
                </thead>
                <tbody>
        `;

        serverLogs.forEach(function (log) {
            const levelColor =
                log.level === "ERROR"
                    ? "#ef4444"
                    : log.level === "WARNING"
                        ? "#f59e0b"
                        : "#38bdf8";

            const formattedTime = new Date(log.created_at).toLocaleString("en-US");

            html += `
                <tr style="border-bottom: 1px solid #334155;">
                    <td style="padding: 10px 5px; color: ${levelColor}; font-weight: bold;">
                        ${log.level}
                    </td>
                    <td style="padding: 10px 5px; color: #e2e8f0;">
                        ${log.message}
                    </td>
                    <td style="padding: 10px 5px; color: #94a3b8; direction: ltr; text-align: right;">
                        ${formattedTime}
                    </td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        tableContainer.innerHTML = html;
    } catch (error) {
        console.error("Error loading logs:", error);

        const tableContainer = document.getElementById("logsTableContainer");

        if (tableContainer) {
            tableContainer.innerHTML = `<p style="color: #ef4444;">Error loading logs.</p>`;
        }
    }
}

// ================================
// Alerts
// ================================

async function loadServerAlerts(serverName) {
    const alertsContent = document.getElementById("alertsContent");

    if (!alertsContent) {
        return;
    }

    alertsContent.innerHTML = `<p style="color: #94a3b8;">Loading alerts...</p>`;

    try {
        const response = await apiFetch(API_ALERTS);
        const data = await response.json();
        const allAlerts = data.results || data;

        const serverAlerts = allAlerts.filter(function (alert) {
            return (
                alert.server_name &&
                serverName &&
                alert.server_name.trim().toLowerCase() === serverName.trim().toLowerCase()
            );
        });

        if (serverAlerts.length === 0) {
            alertsContent.innerHTML = `<p style="color: #22c55e; padding: 10px;">No alerts recorded for this server.</p>`;
            return;
        }

        let html = `<div style="display: flex; flex-direction: column; gap: 15px; width: 100%;">`;

        serverAlerts.forEach(function (alert) {
            const isWarning = alert.level === "WARNING";

            const borderColor = alert.is_active
                ? isWarning ? "#f59e0b" : "#ef4444"
                : "#334155";

            const badgeColor = alert.is_active
                ? isWarning ? "#f59e0b" : "#ef4444"
                : "#94a3b8";

            html += `
                <div style="background: #1e293b; border-left: 4px solid ${borderColor}; padding: 15px; border-radius: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 style="margin: 0; color: #e2e8f0; font-size: 16px;">
                            ${alert.title || "Notification"}
                        </h4>

                        <span style="color: ${badgeColor}; font-size: 12px; font-weight: bold;">
                            ${alert.is_active ? `Active (${alert.level})` : "Resolved"}
                        </span>
                    </div>

                    <p style="margin: 0 0 10px 0; color: #cbd5e1; font-size: 14px; line-height: 1.5;">
                        ${alert.message}
                    </p>

                    <div style="font-size: 12px; color: #64748b; display: flex; gap: 15px;">
                        <span><strong>Target:</strong> ${alert.server_name}</span>
                        ${alert.level ? `<span><strong>Severity:</strong> ${alert.level}</span>` : ""}
                    </div>
                </div>
            `;
        });

        html += `</div>`;

        alertsContent.innerHTML = html;
    } catch (error) {
        console.error("Error loading alerts:", error);
        alertsContent.innerHTML = `<p style="color: #ef4444; padding: 10px;">Error loading alerts.</p>`;
    }
}

// ================================
// Metrics / Chart
// ================================

function showMetricsPage() {
    const tableContainer = document.querySelector(".table-container");
    const pageHeader = document.querySelector(".page-header");
    const metricsPage = document.getElementById("metricsPage");
    const metricsMenuBtn = document.getElementById("metricsMenuBtn");

    if (tableContainer) {
        tableContainer.style.display = "none";
    }

    if (pageHeader) {
        pageHeader.style.display = "none";
    }

    if (metricsPage) {
        metricsPage.style.display = "block";
    }

    document.querySelectorAll(".menu a").forEach(function (link) {
        link.classList.remove("active");
    });

    if (metricsMenuBtn) {
        metricsMenuBtn.classList.add("active");
    }

    generateServerSelector();
}

async function generateServerSelector() {
    const container = document.getElementById("serverSelectorContainer");

    if (!container) {
        return;
    }

    container.innerHTML = `<p style="color: #94a3b8;">Loading servers...</p>`;

    try {
        const response = await apiFetch(API_SERVERS);
        const data = await response.json();
        const servers = data.results || data;

        container.innerHTML = "";

        servers.forEach(function (server, index) {
            const button = document.createElement("button");

            button.textContent = server.hostname;
            button.className = "view-btn";
            button.style.marginRight = "5px";

            button.addEventListener("click", function () {
                document.querySelectorAll("#serverSelectorContainer .view-btn").forEach(function (btn) {
                    btn.style.background = "#38bdf8";
                });

                button.style.background = "#10b981";

                loadChartData(server.id);
            });

            container.appendChild(button);

            if (index === 0) {
                button.click();
            }
        });
    } catch (error) {
        console.error("Error generating server selector:", error);
    }
}

async function loadChartData(serverId) {
    try {
        const response = await apiFetch(`${API_BASE}/api/servers/${serverId}/chart/`);
        const data = await response.json();

        const labels = data.map(function (item) {
            return item.time;
        });

        const cpuData = data.map(function (item) {
            return item.cpu;
        });

        const ramData = data.map(function (item) {
            return item.ram;
        });

        const diskData = data.map(function (item) {
            return item.disk;
        });

        const chartElement = document.getElementById("metricsChart");

        if (!chartElement) {
            return;
        }

        const ctx = chartElement.getContext("2d");

        if (performanceChart) {
            performanceChart.destroy();
        }

        performanceChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "CPU Usage (%)",
                        data: cpuData,
                        borderColor: "#f59e0b",
                        backgroundColor: "rgba(245, 158, 11, 0.1)",
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: "RAM Usage (%)",
                        data: ramData,
                        borderColor: "#22c55e",
                        backgroundColor: "rgba(34, 197, 94, 0.1)",
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: "Disk Usage (%)",
                        data: diskData,
                        borderColor: "#38bdf8",
                        backgroundColor: "rgba(56, 189, 248, 0.1)",
                        borderWidth: 2,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: "#e2e8f0"
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: "#334155"
                        },
                        ticks: {
                            color: "#94a3b8"
                        }
                    },
                    y: {
                        min: 0,
                        max: 100,
                        grid: {
                            color: "#334155"
                        },
                        ticks: {
                            color: "#94a3b8"
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error("Error loading chart data:", error);
    }
}

// ================================
// Logout
// ================================

function logout() {
    clearTokens();
    window.location.href = "/login/";
}

// ================================
// Page Init
// ================================

document.addEventListener("DOMContentLoaded", function () {
    if (!getAccessToken()) {
        redirectToLogin();
        return;
    }

    if (document.getElementById("tableBody")) {
        loadServers();
    }

    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", logout);
    }
});
