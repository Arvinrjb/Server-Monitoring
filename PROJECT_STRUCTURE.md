flowchart TD
    %% Server
    user --> system


    %% Status
 system --> Monitoring
    Monitoring --> Dashboard 
    Monitoring --> Agent_Report 
    Monitoring --> Add_Server 


    %% Logs
 system --> Logs


    %% Alerts
 system --> Alerts


    %% Accounts
    user --> Accounts
 system --> Accounts
    Accounts --> Login  
    Accounts --> Sign_UP 