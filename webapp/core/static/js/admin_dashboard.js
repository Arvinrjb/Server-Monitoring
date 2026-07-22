const API = {
    servers: "/api/servers/",
    add: "/api/addserver/",
    logs: "/api/logs/",
    alerts: "/api/alerts/",
    profiles: "/api/profile/"
};

let selectedProfile = null;
let currentServerId = null;
let performanceChart = null;
let selectedServerForEdit = null;

function getCookie(name) {
    for (const c of (document.cookie || "").split(";")) {
        const t = c.trim();
        if (t.startsWith(`${name}=`)) return decodeURIComponent(t.slice(name.length + 1));
    }
    return null;
}

async function fetchJSON(url, options = {}) {
    const csrf = getCookie("csrftoken");
    const config = {
        ...options,
        credentials: "same-origin",
        headers: {
            Accept: "application/json",
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...(csrf ? { "X-CSRFToken": csrf } : {}),
            ...(options.headers || {})
        }
    };
    const res = await fetch(url, config);
    const ct = res.headers.get("content-type") || "";
    let data = null;
    if (ct.includes("application/json")) data = await res.json();
    else if (res.status !== 204) data = await res.text();
    if (!res.ok) {
        throw new Error(
            (data && typeof data === "object"
                ? data.detail || data.message || JSON.stringify(data)
                : data) || `Request failed with status ${res.status}`
        );
    }
    return data;
}

const norm = (v, fb = "N/A") => (v == null || v === "" ? fb : String(v));
const clamp = v => Math.min(100, Math.max(0, Number(v) || 0));
const list = d => (Array.isArray(d) ? d : Array.isArray(d?.results) ? d.results : []);
const profileList = d => (Array.isArray(d) ? d : Array.isArray(d?.results) ? d.results : d?.id ? [d] : []);

function el(tag, cls, txt) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt !== undefined) e.textContent = txt;
    return e;
}

const $ = id => document.getElementById(id);
const clear = e => { if (e) while (e.firstChild) e.removeChild(e.firstChild); };

function setTableMsg(msg, cls = "empty-state") {
    const tb = $("tableBody");
    if (!tb) return;
    clear(tb);
    const td = el("td", cls, msg);
    td.colSpan = 8;
    const tr = document.createElement("tr");
    tr.appendChild(td);
    tb.appendChild(tr);
}

function setProfilesMsg(msg, cls = "empty-state") {
    const tb = $("profilesTableBody");
    if (!tb) return;
    clear(tb);
    const td = el("td", cls, msg);
    td.colSpan = 5;
    const tr = document.createElement("tr");
    tr.appendChild(td);
    tb.appendChild(tr);
}

function setStatus(id, msg, type) {
    const s = $(id);
    if (!s) return;
    s.textContent = msg || "";
    s.classList.remove("success", "error");
    if (type) s.classList.add(type);
}

function toggleModal(id, open) {
    const m = $(id);
    if (!m) return;
    if (open) {
        m.hidden = false;
        m.classList.add("show");
        m.setAttribute("aria-hidden", "false");
    } else {
        m.classList.remove("show");
        m.hidden = true;
        m.setAttribute("aria-hidden", "true");
    }
}

function getOwnerName(server) {
    if (server.user && typeof server.user === "object") {
        const full = `${norm(server.user.first_name, "")} ${norm(server.user.last_name, "")}`.trim();
        return full || norm(server.user.username);
    }
    return norm(server.user);
}

function createCell(text, cls) {
    const td = el("td", cls);
    td.textContent = norm(text);
    return td;
}

function createUsageCell(value, fillCls) {
    const pct = clamp(value);
    const td = document.createElement("td");
    const fill = el("div", `usage-fill ${fillCls}`);
    fill.style.width = `${pct}%`;
    const bar = el("div", "usage-bar");
    bar.appendChild(fill);
    const wrap = el("div", "usage-cell");
    wrap.appendChild(bar);
    wrap.appendChild(el("span", null, `${pct}%`));
    td.appendChild(wrap);
    return td;
}

function createStatusCell(status) {
    const td = document.createElement("td");
    const s = norm(status, "offline").toLowerCase();
    td.appendChild(el("span", `status-badge ${s}`, s));
    return td;
}

function createAlertCell(hasAlert) {
    const td = document.createElement("td");
    if (hasAlert) {
        const icon = el("span", "alert-icon", "!");
        icon.title = "Active alert";
        td.appendChild(icon);
    } else {
        td.textContent = "-";
    }
    return td;
}

function hasActiveAlert(alerts, server) {
    const hn = norm(server.hostname, "").trim().toLowerCase();
    return alerts.some(a => {
        const an = norm(a.server_name, "").trim().toLowerCase();
        return an && hn && an === hn && a.is_active === true;
    });
}

async function loadServers() {
    setTableMsg("Loading servers...");
    try {
        const [sd, ad] = await Promise.all([fetchJSON(API.servers), fetchJSON(API.alerts)]);
        const servers = list(sd), alerts = list(ad);
        const tb = $("tableBody");
        if (!tb) return;
        clear(tb);
        if (!servers.length) { setTableMsg("No servers found."); return; }
        servers.forEach(server => {
            const row = document.createElement("tr");
            const cpu = server.latest_status?.cpu_usage ?? 0;
            const ram = server.latest_status?.ram_usage ?? 0;
            row.appendChild(createCell(server.hostname ?? ""));
            row.appendChild(createCell(server.ipaddress ?? ""));
            row.appendChild(createCell(getOwnerName(server)));
            row.appendChild(createStatusCell(server.status));
            row.appendChild(createUsageCell(cpu, "cpu-fill"));
            row.appendChild(createUsageCell(ram, "ram-fill"));
            row.appendChild(createAlertCell(hasActiveAlert(alerts, server)));
            const td = document.createElement("td");
            td.classList.add("server-actions");
            const detBtn = el("button", "view-btn", "Details");
            detBtn.type = "button";
            detBtn.addEventListener("click", e => { e.stopPropagation(); showServerDetails(server.id, server); });
            const editBtn = el("button", "edit-btn", "Edit");
            editBtn.type = "button";
            editBtn.addEventListener("click", e => { e.stopPropagation(); showServerEditModal(server); });
            td.appendChild(detBtn);
            td.appendChild(editBtn);
            row.appendChild(td);
            row.addEventListener("click", () => showServerDetails(server.id, server));
            tb.appendChild(row);
        });
    } catch {
        setTableMsg("Error loading servers.", "error-state");
    }
}

async function loadProfiles() {
    setProfilesMsg("Loading profiles...");
    try {
        const profiles = profileList(await fetchJSON(API.profiles));
        const tb = $("profilesTableBody");
        if (!tb) return;
        clear(tb);
        if (!profiles.length) { setProfilesMsg("No profiles found."); return; }
        profiles.forEach(profile => {
            const row = document.createElement("tr");
            ["email", "first_name", "last_name", "phone_number", "telegram_id"].forEach(k => row.appendChild(createCell(profile[k])));
            row.addEventListener("click", () => {
                document.querySelectorAll("#profilesTable tbody tr").forEach(r => r.classList.remove("active"));
                row.classList.add("active");
                showProfileDetails(profile);
            });
            tb.appendChild(row);
        });
    } catch {
        setProfilesMsg("Error loading profiles.", "error-state");
    }
}

function showProfileDetails(profile) {
    selectedProfile = profile;
    const ids = ["profileDetailEmail", "profileDetailId", "profileFirstNameInput", "profileLastNameInput", "profileBioInput", "profilePhoneInput", "profileTelegramInput"];
    const [email, pid, fn, ln, bio, phone, tg] = ids.map($);
    if (!email) return;
    email.textContent = norm(profile.email, "Profile");
    pid.textContent = `Profile ID: ${norm(profile.id)}`;
    fn.value = norm(profile.first_name, "");
    ln.value = norm(profile.last_name, "");
    bio.value = norm(profile.bio, "");
    phone.value = norm(profile.phone_number, "");
    tg.value = norm(profile.telegram_id, "");
    setStatus("profileSaveStatus", "");
    toggleModal("profileModal", true);
    document.body.style.overflow = "hidden";
}

function closeProfileModal() {
    toggleModal("profileModal", false);
    document.body.style.overflow = "";
    setStatus("profileSaveStatus", "");
}

async function updateSelectedProfile(event) {
    event.preventDefault();
    if (!selectedProfile?.id) { setStatus("profileSaveStatus", "No profile selected.", "error"); return; }
    const payload = {
        first_name: $("profileFirstNameInput")?.value.trim() || "",
        last_name: $("profileLastNameInput")?.value.trim() || "",
        bio: $("profileBioInput")?.value.trim() || "",
        phone_number: $("profilePhoneInput")?.value.trim() || "",
        telegram_id: $("profileTelegramInput")?.value.trim() || ""
    };
    setStatus("profileSaveStatus", "Saving...");
    try {
        const updated = await fetchJSON(`${API.profiles}${encodeURIComponent(selectedProfile.id)}/`, {
            method: "PATCH", body: JSON.stringify(payload)
        });
        selectedProfile = { ...selectedProfile, ...updated, ...payload };
        setStatus("profileSaveStatus", "Saved successfully.", "success");
        await loadProfiles();
    } catch (err) {
        setStatus("profileSaveStatus", err.message || "Error saving profile.", "error");
    }
}

function showPage(active) {
    ["mainDashboardView", "metricsPage", "profilesPage"].forEach(id => {
        const el = $(id);
        if (el) el.hidden = id !== active;
    });
    document.querySelectorAll(".menu a").forEach(a => a.classList.remove("active"));
}

function showDashboardPage() {
    showPage("mainDashboardView");
    $("dashboardMenuBtn")?.classList.add("active");
}

function showMetricsPage() {
    showPage("metricsPage");
    $("metricsMenuBtn")?.classList.add("active");
    generateServerSelector();
}

function showProfilesPage() {
    showPage("profilesPage");
    $("profilesMenuBtn")?.classList.add("active");
    loadProfiles();
}

function showServerDetails(id, server) {
    currentServerId = id;
    const modal = $("detailModal");
    const name = $("modalServerName");
    if (!modal || !name) return;
    name.textContent = norm(server.hostname, "Server Details");
    modal.hidden = false;
    modal.classList.add("show");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    openTab(0);
    renderOverview(server);
    loadServerLogs(id);
    loadServerAlerts(norm(server.hostname, ""));
}

function closeDetailModal() {
    toggleModal("detailModal", false);
    if ($("profileModal")?.hidden !== false) document.body.style.overflow = "";
}

function openTab(idx) {
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    $(`tab${idx}`)?.classList.add("active");
    document.querySelector(`.tab-btn[data-tab="${idx}"]`)?.classList.add("active");
}

function addInfoItem(container, label, value) {
    const item = el("div", "info-item");
    item.appendChild(el("span", "info-label", label));
    item.appendChild(el("span", "info-value", norm(value)));
    container.appendChild(item);
}

function renderOverview(server) {
    const oc = $("overviewContent");
    if (!oc) return;
    const grid = el("div", "overview-grid");
    clear(oc);
    addInfoItem(grid, "IP Address", server.ipaddress);
    addInfoItem(grid, "Owner", getOwnerName(server));
    addInfoItem(grid, "OS", server.os);
    addInfoItem(grid, "Status", server.status || "offline");
    addInfoItem(grid, "Agent Token", server.agent_token || "Agent Token");
    addInfoItem(grid, "Lastest Log", server.lastest_log?.message ?? "No logs");
    // addInfoItem(grid, "CPU Usage", `${clamp(server.latest_status?.cpu_usage)}%`);
    // addInfoItem(grid, "RAM Usage", `${clamp(server.latest_status?.ram_usage)}%`);
    // addInfoItem(grid, "DISK Usage", `${clamp(server.latest_status?.disk_usage)}%`);
    oc.appendChild(grid);
}

function renderLogsToolbar(serverId, limit) {
    const wrap = el("div", "logs-toolbar");
    const sel = el("select", "select-control");
    sel.id = "logLimitSelect";
    [10, 20, 50, 100].forEach(v => {
        const opt = el("option", null, `${v} Logs`);
        opt.value = String(v);
        if (Number(limit) === v) opt.selected = true;
        sel.appendChild(opt);
    });
    sel.addEventListener("change", () => loadServerLogs(serverId, Number(sel.value)));
    const controls = document.createElement("div");
    controls.appendChild(el("label", null, "Show: "));
    controls.appendChild(sel);
    wrap.appendChild(el("h3", null, "Server Logs"));
    wrap.appendChild(controls);
    return wrap;
}

function formatDate(v) {
    if (!v) return "N/A";
    const d = new Date(v);
    return isNaN(d.getTime()) ? "N/A" : d.toLocaleString("en-US");
}

function getLevelColor(level) {
    if (level === "ERROR" || level === "CRITICAL") return "#ef4444";
    if (level === "WARNING") return "#f59e0b";
    return "#38bdf8";
}

async function loadServerLogs(serverId, limit = 20) {
    const lc = $("logsContent");
    if (!lc) return;
    clear(lc);
    lc.appendChild(renderLogsToolbar(serverId, limit));
    const container = document.createElement("div");
    container.appendChild(el("p", null, "Loading logs..."));
    lc.appendChild(container);
    try {
        const logs = list(await fetchJSON(`${API.logs}?server=${encodeURIComponent(serverId)}&limit=${encodeURIComponent(limit)}&ordering=-created_at`));
        clear(container);
        if (!logs.length) { container.appendChild(el("p", "empty-state", "No logs found for this server.")); return; }
        const table = el("table", "table-lite");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");
        const hr = document.createElement("tr");
        ["Level", "Message", "Time"].forEach(t => hr.appendChild(el("th", null, t)));
        thead.appendChild(hr);
        logs.forEach(log => {
            const row = document.createElement("tr");
            const lc2 = createCell(log.level);
            const tc = createCell(formatDate(log.created_at));
            lc2.style.color = getLevelColor(log.level);
            lc2.style.fontWeight = "700";
            tc.style.color = "#94a3b8";
            tc.style.direction = "ltr";
            tc.style.textAlign = "right";
            row.appendChild(lc2);
            row.appendChild(createCell(log.message));
            row.appendChild(tc);
            tbody.appendChild(row);
        });
        table.appendChild(thead);
        table.appendChild(tbody);
        container.appendChild(table);
    } catch {
        clear(container);
        container.appendChild(el("p", "error-state", "Error loading logs."));
    }
}

async function loadServerAlerts(serverName) {
    const ac = $("alertsContent");
    if (!ac) return;
    clear(ac);
    ac.appendChild(el("p", null, "Loading alerts..."));
    try {
        const sn = norm(serverName, "").trim().toLowerCase();
        const alerts = list(await fetchJSON(API.alerts))
            .filter(a => norm(a.server_name, "").trim().toLowerCase() === sn && sn);
        clear(ac);
        if (!alerts.length) { ac.appendChild(el("p", "empty-state", "No alerts recorded for this server.")); return; }
        const listEl = el("div", "alert-list");
        alerts.forEach(a => listEl.appendChild(createAlertCard(a)));
        ac.appendChild(listEl);
    } catch {
        clear(ac);
        ac.appendChild(el("p", "error-state", "Error loading alert details."));
    }
}

function createAlertCard(alert) {
    const isActive = alert.is_active === true;
    const stateClass = isActive ? (alert.level === "WARNING" ? "warning" : "critical") : "resolved";
    const card = el("div", `alert-card ${stateClass}`);
    const header = el("div", "alert-card-header");
    header.appendChild(el("h4", null, alert.title || "Notification"));
    header.appendChild(el("span", `alert-badge ${stateClass}`, isActive ? `Active (${norm(alert.level, "ALERT")})` : "Resolved"));
    const meta = el("div", "alert-meta");
    meta.appendChild(el("span", null, `Target: ${norm(alert.server_name)}`));
    if (alert.level) meta.appendChild(el("span", null, `Severity: ${alert.level}`));
    card.appendChild(header);
    card.appendChild(el("p", null, alert.message || "No message provided."));
    card.appendChild(meta);
    return card;
}

async function generateServerSelector() {
    const container = $("serverSelectorContainer");
    if (!container) return;
    clear(container);
    container.appendChild(el("p", null, "Loading servers..."));
    try {
        const servers = list(await fetchJSON(API.servers));
        clear(container);
        if (!servers.length) { container.appendChild(el("p", "empty-state", "No servers found.")); return; }
        servers.forEach((server, i) => {
            const btn = el("button", "selector-btn", norm(server.hostname, `Server ${i + 1}`));
            btn.type = "button";
            btn.addEventListener("click", () => {
                document.querySelectorAll("#serverSelectorContainer .selector-btn").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                loadChartData(server.id);
            });
            container.appendChild(btn);
            if (i === 0) btn.click();
        });
    } catch {
        clear(container);
        container.appendChild(el("p", "error-state", "Error loading servers."));
    }
}

async function loadChartData(serverId) {
    const canvas = $("metricsChart");
    if (!canvas || typeof Chart === "undefined") return;
    try {
        const data = await fetchJSON(`${API.servers}${encodeURIComponent(serverId)}/chart/`);
        const items = Array.isArray(data) ? data : list(data);
        if (performanceChart) performanceChart.destroy();
        performanceChart = new Chart(canvas.getContext("2d"), {
            type: "line",
            data: {
                labels: items.map(i => i.time),
                datasets: [
                    { label: "CPU Usage (%)", data: items.map(i => clamp(i.cpu)), borderColor: "#f59e0b", backgroundColor: "rgba(245,158,11,0.1)", borderWidth: 2, tension: 0.3 },
                    { label: "RAM Usage (%)", data: items.map(i => clamp(i.ram)), borderColor: "#22c55e", backgroundColor: "rgba(34,197,94,0.1)", borderWidth: 2, tension: 0.3 },
                    { label: "Disk Usage (%)", data: items.map(i => clamp(i.disk)), borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,0.1)", borderWidth: 2, tension: 0.3 }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                interaction: { mode: "index", intersect: false },
                plugins: { legend: { labels: { color: "#e2e8f0" } } },
                scales: {
                    x: { grid: { color: "#334155" }, ticks: { color: "#94a3b8" } },
                    y: { min: 0, max: 100, grid: { color: "#334155" }, ticks: { color: "#94a3b8" } }
                }
            }
        });
    } catch { /* silent */ }
}

function openServerEditModal() {
    toggleModal("serverEditModal", true);
}

function closeServerEditModal() {
    toggleModal("serverEditModal", false);
    selectedServerForEdit = null;
    setStatus("serverEditSaveStatus", "");
}

function showServerEditModal(server) {
    if (!server?.id) return;
    const modal = $("serverEditModal");
    if (!modal) return;
    selectedServerForEdit = server;
    const q = s => modal.querySelector(s);
    const title = q("#serverEditTitle");
    const idEl = q("#serverEditId");
    const hn = q("#serverHostnameInput");
    const ip = q("#serverIpInput");
    const os = q("#serverOsInput");
    const st = q("#serverStatusInput");
    if (title) title.textContent = server.hostname || "Edit Server";
    if (idEl) idEl.textContent = `Server ID: ${server.id}`;
    if (hn) hn.value = norm(server.hostname);
    if (ip) ip.value = norm(server.ipaddress);
    if (os) os.value = norm(server.os);
    if (st) st.value = norm(server.status).toLowerCase() === "online" ? "online" : "offline";
    setStatus("serverEditSaveStatus", "");
    openServerEditModal();
}

async function updateSelectedServer(event) {
    event.preventDefault();
    if (!selectedServerForEdit?.id) { setStatus("serverEditSaveStatus", "No server selected.", "error"); return; }
    const modal = $("serverEditModal");
    if (!modal) { setStatus("serverEditSaveStatus", "Edit modal not found.", "error"); return; }
    const q = s => modal.querySelector(s);
    const hostname = q("#serverHostnameInput")?.value.trim() || "";
    const ipaddress = q("#serverIpInput")?.value.trim() || "";
    const os = q("#serverOsInput")?.value.trim() || "";
    const status = q("#serverStatusInput")?.value || "offline";
    if (!hostname || !ipaddress || !os) { setStatus("serverEditSaveStatus", "Hostname, IP address and OS are required.", "error"); return; }
    if (!["online", "offline"].includes(status)) { setStatus("serverEditSaveStatus", "Invalid status value.", "error"); return; }
    setStatus("serverEditSaveStatus", "Saving...");
    try {
        const updated = await fetchJSON(`${API.add}${selectedServerForEdit.id}/`, {
            method: "PATCH", body: JSON.stringify({ hostname, ipaddress, os, status })
        });
        selectedServerForEdit = updated || { ...selectedServerForEdit, hostname, ipaddress, os, status };
        setStatus("serverEditSaveStatus", "Saved successfully.", "success");
        await loadServers();
        setTimeout(closeServerEditModal, 500);
    } catch (err) {
        setStatus("serverEditSaveStatus", err.message || "Failed to save server.", "error");
    }
}

function bindEvents() {
    const on = (id, ev, fn) => $(id)?.addEventListener(ev, fn);
    on("metricsMenuBtn", "click", e => { e.preventDefault(); showMetricsPage(); });
    on("profilesMenuBtn", "click", e => { e.preventDefault(); showProfilesPage(); });
    on("dashboardMenuBtn", "click", e => { e.preventDefault(); showDashboardPage(); });
    on("refreshServersBtn", "click", loadServers);
    on("refreshProfilesBtn", "click", loadProfiles);
    on("profileEditForm", "submit", updateSelectedProfile);
    on("serverEditForm", "submit", updateSelectedServer);
    on("closeDetailModalBtn", "click", closeDetailModal);
    on("closeProfileModalBtn", "click", closeProfileModal);
    on("closeServerEditModalBtn", "click", closeServerEditModal);
    const backdrop = (id, fn) => $(id)?.addEventListener("click", e => { if (e.target === $(id)) fn(); });
    backdrop("detailModal", closeDetailModal);
    backdrop("profileModal", closeProfileModal);
    backdrop("serverEditModal", closeServerEditModal);
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => openTab(Number(btn.dataset.tab)));
    });
    document.addEventListener("keydown", e => {
        if (e.key === "Escape") { closeDetailModal(); closeProfileModal(); closeServerEditModal(); }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    showDashboardPage();
    loadServers();
});
