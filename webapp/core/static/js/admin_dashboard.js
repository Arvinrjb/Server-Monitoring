const API_SERVERS = 'http://127.0.0.1:8000/api/servers/';
const API_LOGS = 'http://127.0.0.1:8000/api/logs/';
const API_ALERTS = 'http://127.0.0.1:8000/api/alerts/';

let currentServerId = null;

// ۱. بارگذاری سرورها و آلرت‌ها در جدول اصلی
async function loadServers() {
    try {
        const [serversRes, alertsRes] = await Promise.all([
            fetch(API_SERVERS),
            fetch(API_ALERTS)
        ]);

        const serversData = await serversRes.json();
        const alertsData = await alertsRes.json();

        const servers = serversData.results || serversData;
        const alerts = alertsData.results || alertsData;

        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        servers.forEach(server => { 
            // بررسی وجود آلرت فعال بدون حساسیت به حروف کوچک و بزرگ
            const hasAlert = alerts.some(alert => 
                alert.server_name && server.hostname &&
                alert.server_name.trim().toLowerCase() === server.hostname.trim().toLowerCase() && 
                alert.is_active === true
            );

            const cpu = server.latest_status?.cpu_usage || 0;
            const ram = server.latest_status?.ram_usage || 0;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${server.hostname}</td>
                <td>${server.ipaddress}</td>
                <td>${server.user?.username || server.user || 'N/A'}</td>
                <td><span class="status-badge ${server.status || 'offline'}">${server.status || 'offline'}</span></td>
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
                <td>${hasAlert ? '<span class="alert-icon" style="color: #ef4444; font-size: 20px;">⚠️</span>' : '—'}</td>
                <td><button class="view-btn" onclick="event.stopPropagation(); showServerDetails('${server.id}', ${JSON.stringify(server).replace(/"/g, '&quot;')})">Details</button></td>
            `;

            row.onclick = () => showServerDetails(server.id, server);
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading servers or alerts:", error);
    }
}

// ۲. نمایش مودال جزئیات سرور و تب‌ها
async function showServerDetails(id, server) {
    currentServerId = id;
    
    // اجرای توابع مربوط به تب‌ها با آرگومان‌های صحیح
    loadServerLogs(id);                  // ارسال ID برای لاگ‌ها
    loadServerAlerts(server.hostname);   // ارسال نام سرور برای آلرت‌ها
    
    document.getElementById('modalServerName').textContent = server.hostname;

    const modal = document.getElementById('detailModal');
    modal.classList.add('show');

    // باز کردن تب Overview به صورت پیش‌فرض
    openTab(0);

    document.getElementById('overviewContent').innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 16px;">
            <p><strong>IP Address:</strong> ${server.ipaddress}</p>
            <p><strong>Owner:</strong> ${server.user?.username || 'N/A'}</p>
            <p><strong>OS:</strong> ${server.os || 'N/A'}</p>
            <p><strong>Status:</strong> <span class="${server.status}">${server.status}</span></p>
        </div>
    `;
}

// ۳. بستن مودال
function closeDetailModal() {
    const modal = document.getElementById('detailModal');
    modal.classList.remove('show');
}

// ۴. مدیریت جابجایی بین تب‌ها
function openTab(tabIndex) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    document.getElementById('tab' + tabIndex).classList.add('active');
    if (buttons[tabIndex]) {
        buttons[tabIndex].classList.add('active');
    }
}

// ۵. بارگذاری لاگ‌ها (با قابلیت دسترسی به صفحات بک‌آند)
async function loadServerLogs(serverId, limit = 20) {
    const logsContent = document.getElementById('logsContent');
    
    logsContent.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="font-size: 16px; color: #38bdf8;">Server Logs</h3>
            <div>
                <label for="logLimitSelect" style="color: #94a3b8; font-size: 14px; margin-right: 8px;">Show:</label>
                <select id="logLimitSelect" onchange="loadServerLogs('${serverId}', this.value)" style="background: #334155; color: #fff; border: 1px solid #475569; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                    <option value="10" ${limit == 10 ? 'selected' : ''}>10 Logs</option>
                    <option value="20" ${limit == 20 ? 'selected' : ''}>20 Logs</option>
                    <option value="50" ${limit == 50 ? 'selected' : ''}>50 Logs</option>
                    <option value="100" ${limit == 100 ? 'selected' : ''}>100 Logs</option>
                </select>
            </div>
        </div>
        <div id="logsTableContainer"><p style="color: #94a3b8;">Loading logs...</p></div>
    `;

    try {
        const res = await fetch(`${API_LOGS}?limit=${limit}&ordering=-created_at`);
        const data = await res.json();
        const allLogs = data.results || data;

        const serverLogs = allLogs.filter(log => String(log.server) === String(serverId));
        const tableContainer = document.getElementById('logsTableContainer');

        if (serverLogs.length === 0) {
            tableContainer.innerHTML = '<p style="color: #94a3b8;">No logs found for this server in the fetched range.</p>';
            return;
        }

        let logsHTML = `
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

        serverLogs.forEach(log => {
            const levelColor = log.level === 'ERROR' ? '#ef4444' : (log.level === 'WARNING' ? '#f59e0b' : '#38bdf8');
            const formattedTime = new Date(log.created_at).toLocaleString('en-US');

            logsHTML += `
                <tr style="border-bottom: 1px solid #334155;">
                    <td style="padding: 10px 5px; color: ${levelColor}; font-weight: bold;">${log.level}</td>
                    <td style="padding: 10px 5px; color: #e2e8f0;">${log.message}</td>
                    <td style="padding: 10px 5px; color: #94a3b8; direction: ltr; text-align: right;">${formattedTime}</td>
                </tr>
            `;
        });

        logsHTML += '</tbody></table>';
        tableContainer.innerHTML = logsHTML;

    } catch (error) {
        console.error("Error loading server logs:", error);
        document.getElementById('logsTableContainer').innerHTML = '<p style="color: #ef4444;">Error loading logs.</p>';
    }
}

// ۶. بارگذاری و نمایش کامل آلرت‌های مربوط به سرور
async function loadServerAlerts(serverName) {
    const alertsContent = document.getElementById('alertsContent');
    alertsContent.innerHTML = '<p style="color: #94a3b8;">Loading alerts...</p>';

    try {
        const res = await fetch(API_ALERTS);
        const data = await res.json();
        const allAlerts = data.results || data;

        // فیلتر کردن دقیق بر اساس نام بدون حساسیت به فضاهای خالی و بزرگی حروف
        const serverAlerts = allAlerts.filter(alert => 
            alert.server_name && serverName && 
            alert.server_name.trim().toLowerCase() === serverName.trim().toLowerCase()
        );

        if (serverAlerts.length === 0) {
            alertsContent.innerHTML = '<p style="color: #22c55e; padding: 10px;">No alerts recorded for this server.</p>';
            return;
        }

        let alertsHTML = `<div style="display: flex; flex-direction: column; gap: 15px; width: 100%;">`;

        serverAlerts.forEach(alert => {
            const isWarning = alert.level === 'WARNING';
            const borderColor = alert.is_active ? (isWarning ? '#f59e0b' : '#ef4444') : '#334155';
            const badgeBg = alert.is_active ? (isWarning ? 'rgba(245, 158, 11, 0.2)' : 'rgba(239, 68, 68, 0.2)') : 'rgba(71, 85, 105, 0.2)';
            const badgeColor = alert.is_active ? (isWarning ? '#f59e0b' : '#ef4444') : '#94a3b8';

            alertsHTML += `
                <div style="background: #1e293b; border-left: 4px solid ${borderColor}; padding: 15px; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 style="margin: 0; color: #e2e8f0; font-size: 16px; font-weight: bold;">${alert.title || 'Notification'}</h4>
                        <span style="background: ${badgeBg}; color: ${badgeColor}; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                            ${alert.is_active ? `🔴 Active (${alert.level})` : '🟢 Resolved'}
                        </span>
                    </div>
                    <p style="margin: 0 0 10px 0; color: #cbd5e1; font-size: 14px; line-height: 1.5;">
                        ${alert.message}
                    </p>
                    <div style="font-size: 12px; color: #64748b; display: flex; gap: 15px;">
                        <span><strong>Target:</strong> ${alert.server_name}</span>
                        ${alert.level ? `<span><strong>Severity:</strong> ${alert.level}</span>` : ''}
                    </div>
                </div>
            `;
        });

        alertsHTML += '</div>';
        alertsContent.innerHTML = alertsHTML;

    } catch (error) {
        console.error("Error loading server alerts:", error);
        alertsContent.innerHTML = '<p style="color: #ef4444; padding: 10px;">Error loading alerts details.</p>';
    }
}

// ۷. دریافت توکن CSRF (در صورت نیاز به درخواست‌های ارسالی به Django)
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
// تعریف یک متغیر گلوبال برای نگهداری شیء نمودار تا در صورت تغییر سرور، نمودار قبلی ریست شود
let performanceChart = null;

// تابع جابجایی به صفحه چارت‌ها
function showMetricsPage() {
    // پنهان کردن جدول اصلی سرورها
    document.querySelector('.table-container').style.display = 'none';
    document.querySelector('.page-header').style.display = 'none';
    
    // نمایش بخش چارت
    document.getElementById('metricsPage').style.display = 'block';
    
    // فعال کردن کلاس active در سایدبار
    document.querySelectorAll('.menu a').forEach(a => a.classList.remove('active'));
    document.getElementById('metricsMenuBtn').classList.add('active');
    
    // ساخت دکمه‌های انتخاب سرور
    generateServerSelector();
}

// تابع ساخت دکمه برای هر سرور جهت سوئیچ سریع
async function generateServerSelector() {
    const container = document.getElementById('serverSelectorContainer');
    container.innerHTML = '<p style="color: #94a3b8;">Loading servers...</p>';
    
    try {
        const res = await fetch(API_SERVERS);
        const servers = await res.json();
        const serverList = servers.results || servers;
        
        container.innerHTML = '';
        
        serverList.forEach((server, index) => {
            const btn = document.createElement('button');
            btn.textContent = server.hostname;
            btn.className = 'view-btn'; // استفاده از استایل دکمه‌های قبلی شما
            btn.style.marginRight = '5px';
            btn.onclick = () => {
                // هایلایت کردن دکمه فعال
                document.querySelectorAll('#serverSelectorContainer .view-btn').forEach(b => b.style.background = '#38bdf8');
                btn.style.background = '#10b981'; // رنگ سبز برای سرور انتخاب شده
                
                // لود کردن چارت برای سرور انتخاب شده
                loadChartData(server.id);
            };
            container.appendChild(btn);
            
            // به صورت پیش‌فرض چارت اولین سرور را لود کند
            if (index === 0) btn.click();
        });
    } catch (error) {
        console.error("Error generating server selector:", error);
    }
}

// تابع دریافت داده‌ها و رسم نمودار Chart.js
async function loadChartData(serverId) {
    try {
        // ایجاد درخواست به آدرس داینامیک سرور انتخاب شده
        const res = await fetch(`http://127.0.0.1:8000/api/servers/${serverId}/chart/`);
        const data = await res.json();
        
        // استخراج آرایه‌ها برای نمودار
        const labels = data.map(item => item.time);
        const cpuData = data.map(item => item.cpu);
        const ramData = data.map(item => item.ram);
        const diskData = data.map(item => item.disk);
        
        const ctx = document.getElementById('metricsChart').getContext('2d');
        
        // اگر از قبل نموداری رسم شده، آن را حذف کن تا تداخل حافظه ایجاد نشود
        if (performanceChart) {
            performanceChart.destroy();
        }
        
        // ساخت چارت جدید
        performanceChart = new Chart(ctx, {
            type: 'line', // نوع نمودار خطی
            data: {
                labels: labels, // محور افقی (زمان)
                datasets: [
                    {
                        label: 'CPU Usage (%)',
                        data: cpuData,
                        borderColor: '#f59e0b', // رنگ زرد (هماهنگ با پروگرس‌بار شما)
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        tension: 0.3 // نرمی خطوط نمودار
                    },
                    {
                        label: 'RAM Usage (%)',
                        data: ramData,
                        borderColor: '#22c55e', // رنگ سبز
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderWidth: 2,
                        tension: 0.3
                    },
                    {
                        label: 'Disk Usage (%)',
                        data: diskData,
                        borderColor: '#38bdf8', // رنگ آبی مدرن
                        backgroundColor: 'rgba(56, 189, 248, 0.1)',
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
                        labels: { color: '#e2e8f0' } // رنگ متون راهنمای بالای چارت
                    }
                },
                scales: {
                    x: {
                        grid: { color: '#334155' }, // رنگ خطوط شبکه
                        ticks: { color: '#94a3b8' }
                    },
                    y: {
                        min: 0,
                        max: 100, // سقف ۱۰۰ درصد برای ریسورس‌ها
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


// لود اولیه پروژه
document.addEventListener('DOMContentLoaded', () => {
    loadServers();
});