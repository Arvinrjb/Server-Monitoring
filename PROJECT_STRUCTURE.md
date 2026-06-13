flowchart TD
 %% server
 user --> server


 %% Status
 server --> Monitoring
 Monitoring --> Dashboard 
 Monitoring -->|API| Agent_Report 


 %% Logs
 server --> Logs
 Logs --> |API| ShowLogs
 Logs --> |API| AgentLogs


 %% Alerts
 server --> Alerts


 %% Accounts
 user --> Accounts
 Accounts --> Login  
 Accounts --> Sign_UP 