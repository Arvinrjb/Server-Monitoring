flowchart TD
    %% server
    user --> server
    server -->|API| AddServer
    
    

    %% Status
 server --> Monitoring
    Monitoring --> Dashboard 
    Monitoring -->|API| Agent_Report 


    %% Logs
 server --> Logs


    %% Alerts
 server --> Alerts


    %% Accounts
    user --> Accounts
    Accounts --> Login  
    Accounts --> Sign_UP 