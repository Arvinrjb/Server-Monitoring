# Overview
This monitoring system is designed to track server performance and health metrics. It follows a Push-based architecture, where client-side agents report data to a central API server for processing, storage, and alerting.

## System Components
- Agent: A lightweight script installed on target servers that collects metrics (CPU, RAM, Disk, etc.) and system logs, then pushes them to the backend API.
- Backend API (Django): The core service that handles incoming data, performs validation, and orchestrates status updates.
- Alert Engine: Monitors incoming data for thresholds (>90%) and generates alert records in the database.

## APIs
#### To retrieve server information, update data, and add a new server.
- /api/addserver/<br>
- /api/addserver/server_id/<br>

#### To see some server information, latest status, latest log and retrieving the chart for the last 24 hours.
- /api/servers/
- /api/servers/server_id/chart/
- /api/servers/status_id/

#### To view alerts
- api/alerts/

#### To view logs
- api/logs/


#### To retrieve user information and modify certain details
- api/profile/
- api/profile/user_id/

#### To obtain the access and refresh tokens
- api/token/
- api/token/refresh 

#### To send data from the agent (accepts only the POST method)
- api/agent/status/report/ 
- api/agent/logs/report/ 

### [Configurations](configurations.md)