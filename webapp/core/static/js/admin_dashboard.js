const API_SERVERS = "/api/servers/";
const API_LOGS = "/api/logs/";
const API_ALERTS = "/api/alerts/";
const API_PROFILES = "/api/profile/";

let selectedProfile = null;
let currentServerId = null;
let performanceChart = null;

async function fetchJSON(url) {
    const response = await fetch(url, {
        headers: {
            Accept: "application/json"
        },
        credentials: "same-origin"
    });

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
    }

    return response.json();
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(`${name}=`)) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

function getListPayload(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (data && Array.isArray(data.results)) {
        return data.results;
    }

    return [];
}

function getProfilePayload(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (data && Array.isArray(data.results)) {
        return data.results;
    }

    if (data && typeof data === "object" && data.id) {
        return [data];
    }

    return [];
}

function clampPercent(value) {
    const number = Number(value) || 0;
    return Math.min(100, Math.max(0, number));
}

function normalizeText(value, fallback = "N/A") {
    if (value === null || value === undefined || value === "") {
        return fallback;
    }

    return String(value);
}

function clearElement(element) {
    if (!element) {
        return;
    }

    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function createElement(tagName, className, text) {
    const element = document.createElement(tagName);

    if (className) {
        element.className = className;
    }

    if (text !== undefined) {
        element.textContent = text;
    }

    return element;
}

function createCell(text, className) {
    const td = createElement("td", className);
    td.textContent = normalizeText(text);
    return td;
}

function setTableMessage(message, className = "empty-state") {
    const tbody = document.getElementById("tableBody");
    if (!tbody) {
        return;
    }

    clearElement(tbody);

    const row = document.createElement("tr");
    const cell = createElement("td", className, message);
    cell.colSpan = 8;

    row.appendChild(cell);
    tbody.appendChild(row);
}

function setProfilesMessage(message, className = "empty-state") {
    const tbody = document.getElementById("profilesTableBody");
    if (!tbody) {
        return;
    }

    clearElement(tbody);

    const row = document.createElement("tr");
    const cell = createElement("td", className, message);
    cell.colSpan = 5;

    row.appendChild(cell);
    tbody.appendChild(row);
}

function setProfileSaveStatus(message, type) {
    const status = document.getElementById("profileSaveStatus");
    if (!status) {
        return;
    }

    status.textContent = message || "";
    status.classList.remove("success", "error");

    if (type) {
        status.classList.add(type);
    }
}

function openProfileModal() {
    const modal = document.getElementById("profileModal");
    if (!modal) {
        return;
    }

    modal.hidden = false;
    modal.classList.add("show");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}

function closeProfileModal() {
    const modal = document.getElementById("profileModal");
    if (!modal) {
        return;
    }

    modal.classList.remove("show");
    modal.setAttribute("aria-hidden", "true");
    modal.hidden = true;
    document.body.style.overflow = "";
    setProfileSaveStatus("");
}

function getOwnerName(server) {
    if (server.user && typeof server.user === "object") {
        if (server.user.first_name || server.user.last_name) {
            return `${normalizeText(server.user.first_name, "")} ${normalizeText(server.user.last_name, "")}`.trim() || normalizeText(server.user.username);
        }

        return normalizeText(server.user.username);
    }

    return normalizeText(server.user);
}

function createUsageCell(value, fillClass) {
    const percent = clampPercent(value);
    const td = createElement("td");
    const wrapper = createElement("div", "usage-cell");
    const bar = createElement("div", "usage-bar");
    const fill = createElement("div", `usage-fill ${fillClass}`);
    const label = createElement("span", null, `${percent}%`);

    fill.style.width = `${percent}%`;

    bar.appendChild(fill);
    wrapper.appendChild(bar);
    wrapper.appendChild(label);
    td.appendChild(wrapper);

    return td;
}

function createStatusCell(status) {
    const td = document.createElement("td");
    const normalizedStatus = normalizeText(status, "offline").toLowerCase();
    const badge = createElement("span", `status-badge ${normalizedStatus}`, normalizedStatus);

    td.appendChild(badge);
    return td;
}

function createAlertCell(hasAlert) {
    const td = document.createElement("td");

    if (hasAlert) {
        const icon = createElement("span", "alert-icon", "!");
        icon.title = "Active alert";
        td.appendChild(icon);
    } else {
        td.textContent = "-";
    }

    return td;
}

function createActionsCell(server) {
    const td = document.createElement("td");
    const button = createElement("button", "view-btn", "Details");

    button.type = "button";
    button.addEventListener("click", event => {
        event.stopPropagation();
        showServerDetails(server.id, server);
    });

    td.appendChild(button);
    return td;
}

function hasActiveAlertForServer(alerts, server) {
    const hostname = normalizeText(server.hostname, "").trim().toLowerCase();

    return alerts.some(alert => {
        const alertServerName = normalizeText(alert.server_name, "").trim().toLowerCase();
        return alertServerName && hostname && alertServerName === hostname && alert.is_active === true;
    });
}

async function loadServers() {
    setTableMessage("Loading servers...");

    try {
        const [serversData, alertsData] = await Promise.all([
            fetchJSON(API_SERVERS),
            fetchJSON(API_ALERTS)
        ]);

        const servers = getListPayload(serversData);
        const alerts = getListPayload(alertsData);
        const tbody = document.getElementById("tableBody");

        if (!tbody) {
            return;
        }

        clearElement(tbody);

        if (servers.length === 0) {
            setTableMessage("No servers found.");
            return;
        }

        servers.forEach(server => {
            const row = document.createElement("tr");
            const cpu = server.latest_status ? server.latest_status.cpu_usage : 0;
            const ram = server.latest_status ? server.latest_status.ram_usage : 0;

            row.appendChild(createCell(server.hostname));
            row.appendChild(createCell(server.ipaddress));
            row.appendChild(createCell(getOwnerName(server)));
            row.appendChild(createStatusCell(server.status));
            row.appendChild(createUsageCell(cpu, "cpu-fill"));
            row.appendChild(createUsageCell(ram, "ram-fill"));
            row.appendChild(createAlertCell(hasActiveAlertForServer(alerts, server)));
            row.appendChild(createActionsCell(server));

            row.addEventListener("click", () => {
                showServerDetails(server.id, server);
            });

            tbody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading servers:", error);
        setTableMessage("Error loading servers.", "error-state");
    }
}

async function loadProfiles() {
    setProfilesMessage("Loading profiles...");

    try {
        const data = await fetchJSON(API_PROFILES);
        const profiles = getProfilePayload(data);
        const tbody = document.getElementById("profilesTableBody");

        if (!tbody) {
            return;
        }

        clearElement(tbody);

        if (profiles.length === 0) {
            setProfilesMessage("No profiles found.");
            return;
        }

        profiles.forEach(profile => {
            const row = document.createElement("tr");

            row.appendChild(createCell(profile.email));
            row.appendChild(createCell(profile.first_name));
            row.appendChild(createCell(profile.last_name));
            row.appendChild(createCell(profile.phone_number));
            row.appendChild(createCell(profile.telegram_id));

            row.addEventListener("click", () => {
                document.querySelectorAll("#profilesTable tbody tr").forEach(item => {
                    item.classList.remove("active");
                });

                row.classList.add("active");
                showProfileDetails(profile);
            });

            tbody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading profiles:", error);
        setProfilesMessage("Error loading profiles.", "error-state");
    }
}

function showProfileDetails(profile) {
    selectedProfile = profile;

    const profileDetailEmail = document.getElementById("profileDetailEmail");
    const profileDetailId = document.getElementById("profileDetailId");
    const profileFirstNameInput = document.getElementById("profileFirstNameInput");
    const profileLastNameInput = document.getElementById("profileLastNameInput");
    const profileBioInput = document.getElementById("profileBioInput");
    const profilePhoneInput = document.getElementById("profilePhoneInput");
    const profileTelegramInput = document.getElementById("profileTelegramInput");

    if (!profileDetailEmail || !profileDetailId || !profileFirstNameInput || !profileLastNameInput || !profileBioInput || !profilePhoneInput || !profileTelegramInput) {
        return;
    }
    profileDetailEmail.textContent = normalizeText(profile.email, "Profile");
    profileDetailId.textContent = `Profile ID: ${normalizeText(profile.id)}`;
    profileFirstNameInput.value = normalizeText(profile.first_name, "");
    profileLastNameInput.value = normalizeText(profile.last_name, "");
    profileBioInput.value = normalizeText(profile.bio, "");
    profilePhoneInput.value = normalizeText(profile.phone_number, "");
    profileTelegramInput.value = normalizeText(profile.telegram_id, "");
    setProfileSaveStatus("");
    openProfileModal();
}

async function updateSelectedProfile(event) {
    event.preventDefault();

    if (!selectedProfile || !selectedProfile.id) {
        setProfileSaveStatus("No profile selected.", "error");
        return;
    }

    const payload = {
        first_name: document.getElementById("profileFirstNameInput")?.value.trim() || "",
        last_name: document.getElementById("profileLastNameInput")?.value.trim() || "",
        bio: document.getElementById("profileBioInput")?.value.trim() || "",
        phone_number: document.getElementById("profilePhoneInput")?.value.trim() || "",
        telegram_id: document.getElementById("profileTelegramInput")?.value.trim() || ""
    };

    setProfileSaveStatus("Saving...");

    try {
        const response = await fetch(`${API_PROFILES}${encodeURIComponent(selectedProfile.id)}/`, {
            method: "PATCH",
            credentials: "same-origin",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const updatedProfile = await response.json();

        selectedProfile = {
            ...selectedProfile,
            ...updatedProfile,
            ...payload
        };

        setProfileSaveStatus("Saved successfully.", "success");
        await loadProfiles();
    } catch (error) {
        console.error("Error updating profile:", error);
        setProfileSaveStatus("Error saving profile.", "error");
    }
}

function showDashboardPage() {
    const mainDashboardView = document.getElementById("mainDashboardView");
    const metricsPage = document.getElementById("metricsPage");
    const profilesPage = document.getElementById("profilesPage");

    if (mainDashboardView) {
        mainDashboardView.hidden = false;
    }

    if (metricsPage) {
        metricsPage.hidden = true;
    }

    if (profilesPage) {
        profilesPage.hidden = true;
    }

    document.querySelectorAll(".menu a").forEach(link => link.classList.remove("active"));
    document.getElementById("dashboardMenuBtn")?.classList.add("active");
}

function showMetricsPage() {
    const mainDashboardView = document.getElementById("mainDashboardView");
    const metricsPage = document.getElementById("metricsPage");
    const profilesPage = document.getElementById("profilesPage");

    if (mainDashboardView) {
        mainDashboardView.hidden = true;
    }

    if (metricsPage) {
        metricsPage.hidden = false;
    }

    if (profilesPage) {
        profilesPage.hidden = true;
    }

    document.querySelectorAll(".menu a").forEach(link => link.classList.remove("active"));
    document.getElementById("metricsMenuBtn")?.classList.add("active");

    generateServerSelector();
}

function showProfilesPage() {
    const mainDashboardView = document.getElementById("mainDashboardView");
    const metricsPage = document.getElementById("metricsPage");
    const profilesPage = document.getElementById("profilesPage");

    if (mainDashboardView) {
        mainDashboardView.hidden = true;
    }

    if (metricsPage) {
        metricsPage.hidden = true;
    }

    if (profilesPage) {
        profilesPage.hidden = false;
    }

    document.querySelectorAll(".menu a").forEach(link => link.classList.remove("active"));
    document.getElementById("profilesMenuBtn")?.classList.add("active");

    loadProfiles();
}

function showServerDetails(id, server) {
    currentServerId = id;

    const modal = document.getElementById("detailModal");
    const modalServerName = document.getElementById("modalServerName");

    if (!modal || !modalServerName) {
        return;
    }

    modalServerName.textContent = normalizeText(server.hostname, "Server Details");
    modal.hidden = false;
    modal.classList.add("show");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";

    openTab(0);
    renderOverview(server);
    loadServerLogs(id);
    loadServerAlerts(server.hostname);
}

function closeDetailModal() {
    const modal = document.getElementById("detailModal");
    if (!modal) {
        return;
    }

    modal.classList.remove("show");
    modal.setAttribute("aria-hidden", "true");
    modal.hidden = true;

    if (document.getElementById("profileModal")?.hidden !== false) {
        document.body.style.overflow = "";
    }
}

function openTab(tabIndex) {
    document.querySelectorAll(".tab-content").forEach(content => {
        content.classList.remove("active");
    });

    document.querySelectorAll(".tab-btn").forEach(button => {
        button.classList.remove("active");
    });

    const tab = document.getElementById(`tab${tabIndex}`);
    const button = document.querySelector(`.tab-btn[data-tab="${tabIndex}"]`);

    if (tab) {
        tab.classList.add("active");
    }

    if (button) {
        button.classList.add("active");
    }
}

function addInfoItem(container, label, value) {
    const item = createElement("div", "info-item");
    const labelElement = createElement("span", "info-label", label);
    const valueElement = createElement("span", "info-value", normalizeText(value));

    item.appendChild(labelElement);
    item.appendChild(valueElement);
    container.appendChild(item);
}

function renderOverview(server) {
    const overviewContent = document.getElementById("overviewContent");
    if (!overviewContent) {
        return;
    }

    const grid = createElement("div", "overview-grid");

    clearElement(overviewContent);

    addInfoItem(grid, "IP Address", server.ipaddress);
    addInfoItem(grid, "Owner", getOwnerName(server));
    addInfoItem(grid, "OS", server.os);
    addInfoItem(grid, "Status", server.status || "offline");
    addInfoItem(grid, "CPU Usage", `${clampPercent(server.latest_status?.cpu_usage)}%`);
    addInfoItem(grid, "RAM Usage", `${clampPercent(server.latest_status?.ram_usage)}%`);

    overviewContent.appendChild(grid);
}

function renderLogsToolbar(serverId, limit) {
    const wrapper = createElement("div", "logs-toolbar");
    const title = createElement("h3", null, "Server Logs");
    const controls = createElement("div");
    const label = createElement("label", null, "Show: ");
    const select = createElement("select", "select-control");

    select.id = "logLimitSelect";

    [10, 20, 50, 100].forEach(value => {
        const option = createElement("option", null, `${value} Logs`);
        option.value = String(value);

        if (Number(limit) === value) {
            option.selected = true;
        }

        select.appendChild(option);
    });

    select.addEventListener("change", () => {
        loadServerLogs(serverId, Number(select.value));
    });

    controls.appendChild(label);
    controls.appendChild(select);
    wrapper.appendChild(title);
    wrapper.appendChild(controls);

    return wrapper;
}

async function loadServerLogs(serverId, limit = 20) {
    const logsContent = document.getElementById("logsContent");
    if (!logsContent) {
        return;
    }

    clearElement(logsContent);

    logsContent.appendChild(renderLogsToolbar(serverId, limit));

    const tableContainer = createElement("div");
    tableContainer.appendChild(createElement("p", null, "Loading logs..."));
    logsContent.appendChild(tableContainer);

    try {
        let data;
        let serverLogs = [];

        try {
            data = await fetchJSON(`${API_LOGS}?server=${encodeURIComponent(serverId)}&limit=${encodeURIComponent(limit)}&ordering=-created_at`);
            serverLogs = getListPayload(data);
        } catch {
            serverLogs = [];
        }

        if (serverLogs.length === 0) {
            const fallbackData = await fetchJSON(`${API_LOGS}?limit=${encodeURIComponent(limit)}&ordering=-created_at`);
            serverLogs = getListPayload(fallbackData).filter(log => String(log.server) === String(serverId));
        }

        clearElement(tableContainer);

        if (serverLogs.length === 0) {
            tableContainer.appendChild(createElement("p", "empty-state", "No logs found for this server."));
            return;
        }

        const table = createElement("table", "table-lite");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");
        const headerRow = document.createElement("tr");

        ["Level", "Message", "Time"].forEach(text => {
            headerRow.appendChild(createElement("th", null, text));
        });

        thead.appendChild(headerRow);

        serverLogs.forEach(log => {
            const row = document.createElement("tr");
            const levelCell = createCell(log.level);
            const messageCell = createCell(log.message);
            const timeCell = createCell(formatDate(log.created_at));

            levelCell.style.color = getLevelColor(log.level);
            levelCell.style.fontWeight = "700";
            timeCell.style.color = "#94a3b8";
            timeCell.style.direction = "ltr";
            timeCell.style.textAlign = "right";

            row.appendChild(levelCell);
            row.appendChild(messageCell);
            row.appendChild(timeCell);
            tbody.appendChild(row);
        });

        table.appendChild(thead);
        table.appendChild(tbody);
        tableContainer.appendChild(table);
    } catch (error) {
        console.error("Error loading server logs:", error);
        clearElement(tableContainer);
        tableContainer.appendChild(createElement("p", "error-state", "Error loading logs."));
    }
}

async function loadServerAlerts(serverName) {
    const alertsContent = document.getElementById("alertsContent");
    if (!alertsContent) {
        return;
    }

    clearElement(alertsContent);
    alertsContent.appendChild(createElement("p", null, "Loading alerts..."));

    try {
        const data = await fetchJSON(API_ALERTS);
        const alerts = getListPayload(data);
        const normalizedServerName = normalizeText(serverName, "").trim().toLowerCase();

        const serverAlerts = alerts.filter(alert => {
            const alertServerName = normalizeText(alert.server_name, "").trim().toLowerCase();
            return alertServerName && normalizedServerName && alertServerName === normalizedServerName;
        });

        clearElement(alertsContent);

        if (serverAlerts.length === 0) {
            alertsContent.appendChild(createElement("p", "empty-state", "No alerts recorded for this server."));
            return;
        }

        const list = createElement("div", "alert-list");

        serverAlerts.forEach(alert => {
            list.appendChild(createAlertCard(alert));
        });

        alertsContent.appendChild(list);
    } catch (error) {
        console.error("Error loading server alerts:", error);
        clearElement(alertsContent);
        alertsContent.appendChild(createElement("p", "error-state", "Error loading alert details."));
    }
}

function createAlertCard(alert) {
    const isWarning = alert.level === "WARNING";
    const isActive = alert.is_active === true;
    const stateClass = isActive ? (isWarning ? "warning" : "critical") : "resolved";

    const card = createElement("div", `alert-card ${stateClass}`);
    const header = createElement("div", "alert-card-header");
    const title = createElement("h4", null, alert.title || "Notification");
    const badge = createElement("span", `alert-badge ${stateClass}`, isActive ? `Active (${normalizeText(alert.level, "ALERT")})` : "Resolved");
    const message = createElement("p", null, alert.message || "No message provided.");
    const meta = createElement("div", "alert-meta");
    const target = createElement("span", null, `Target: ${normalizeText(alert.server_name)}`);

    header.appendChild(title);
    header.appendChild(badge);
    meta.appendChild(target);

    if (alert.level) {
        meta.appendChild(createElement("span", null, `Severity: ${alert.level}`));
    }

    card.appendChild(header);
    card.appendChild(message);
    card.appendChild(meta);

    return card;
}

function getLevelColor(level) {
    if (level === "ERROR" || level === "CRITICAL") {
        return "#ef4444";
    }

    if (level === "WARNING") {
        return "#f59e0b";
    }

    return "#38bdf8";
}

function formatDate(value) {
    if (!value) {
        return "N/A";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "N/A";
    }

    return date.toLocaleString("en-US");
}

async function generateServerSelector() {
    const container = document.getElementById("serverSelectorContainer");
    if (!container) {
        return;
    }

    clearElement(container);
    container.appendChild(createElement("p", null, "Loading servers..."));

    try {
        const data = await fetchJSON(API_SERVERS);
        const servers = getListPayload(data);

        clearElement(container);

        if (servers.length === 0) {
            container.appendChild(createElement("p", "empty-state", "No servers found."));
            return;
        }

        servers.forEach((server, index) => {
            const button = createElement("button", "selector-btn", normalizeText(server.hostname, `Server ${index + 1}`));
            button.type = "button";

            button.addEventListener("click", () => {
                document.querySelectorAll("#serverSelectorContainer .selector-btn").forEach(item => {
                    item.classList.remove("active");
                });

                button.classList.add("active");
                loadChartData(server.id);
            });

            container.appendChild(button);

            if (index === 0) {
                button.click();
            }
        });
    } catch (error) {
        console.error("Error generating server selector:", error);
        clearElement(container);
        container.appendChild(createElement("p", "error-state", "Error loading servers."));
    }
}

async function loadChartData(serverId) {
    const canvas = document.getElementById("metricsChart");
    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    try {
        const data = await fetchJSON(`${API_SERVERS}${encodeURIComponent(serverId)}/chart/`);
        const chartItems = Array.isArray(data) ? data : getListPayload(data);

        const labels = chartItems.map(item => item.time);
        const cpuData = chartItems.map(item => clampPercent(item.cpu));
        const ramData = chartItems.map(item => clampPercent(item.ram));
        const diskData = chartItems.map(item => clampPercent(item.disk));

        const ctx = canvas.getContext("2d");

        if (performanceChart) {
            performanceChart.destroy();
        }

        performanceChart = new Chart(ctx, {
            type: "line",
            data: {
                labels,
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
                interaction: {
                    mode: "index",
                    intersect: false
                },
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

function bindEvents() {
    const metricsMenuBtn = document.getElementById("metricsMenuBtn");
    const profilesMenuBtn = document.getElementById("profilesMenuBtn");
    const dashboardMenuBtn = document.getElementById("dashboardMenuBtn");
    const refreshServersBtn = document.getElementById("refreshServersBtn");
    const refreshProfilesBtn = document.getElementById("refreshProfilesBtn");
    const profileEditForm = document.getElementById("profileEditForm");
    const closeDetailModalBtn = document.getElementById("closeDetailModalBtn");
    const closeProfileModalBtn = document.getElementById("closeProfileModalBtn");
    const detailModal = document.getElementById("detailModal");
    const profileModal = document.getElementById("profileModal");

    if (metricsMenuBtn) {
        metricsMenuBtn.addEventListener("click", event => {
            event.preventDefault();
            showMetricsPage();
        });
    }

    if (profilesMenuBtn) {
        profilesMenuBtn.addEventListener("click", event => {
            event.preventDefault();
            showProfilesPage();
        });
    }

    if (dashboardMenuBtn) {
        dashboardMenuBtn.addEventListener("click", event => {
            event.preventDefault();
            showDashboardPage();
        });
    }

    if (refreshServersBtn) {
        refreshServersBtn.addEventListener("click", () => {
            loadServers();
        });
    }

    if (refreshProfilesBtn) {
        refreshProfilesBtn.addEventListener("click", () => {
            loadProfiles();
        });
    }

    if (profileEditForm) {
        profileEditForm.addEventListener("submit", updateSelectedProfile);
    }

    if (closeDetailModalBtn) {
        closeDetailModalBtn.addEventListener("click", () => {
            closeDetailModal();
        });
    }

    if (closeProfileModalBtn) {
        closeProfileModalBtn.addEventListener("click", () => {
            closeProfileModal();
        });
    }

    if (detailModal) {
        detailModal.addEventListener("click", event => {
            if (event.target === detailModal) {
                closeDetailModal();
            }
        });
    }

    if (profileModal) {
        profileModal.addEventListener("click", event => {
            if (event.target === profileModal) {
                closeProfileModal();
            }
        });
    }

    document.querySelectorAll(".tab-btn").forEach(button => {
        button.addEventListener("click", () => {
            openTab(Number(button.dataset.tab));
        });
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            closeDetailModal();
            closeProfileModal();
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    showDashboardPage();
    loadServers();
});
