# Configurations for setup

### create .env:
#### Create a file named `.env` in the root directory and assign these values ​​within it:<br>
DJANGO_SECRET_KEY = "your secret key"<br>
DJANGO_DEBUG = "True or empty"<br>
TIME_ZONE = "your time zone"<br>
DB_NAME = "your database name"<br>
DB_PASSWORD = "your database password"<br>
DB_USER = "your database username"<br>
DB_HOST = database host - for local 127.0.0.1 <br>
DB_PORT = database port - for postgresSQL 5432 

### agent/main.py:
#### This script runs on servers, and this entire directory must be copied to the target server.
#### assign these values ​​within it:<br>
BASE_URL = "your base url" (example: http://localhost)<br>
STATUS_URL = f"{BASE_URL}/api/agent/status/report/"<br>
LOGS_URL = f"{BASE_URL}/api/agent/logs/report/"<br>
TOKEN = "your server Token"<br>
#### To obtain the server token, you need to view it via the dashboard or the API (I haven't fixed it yet; I'll fix it by tomorrow!).


### [Architecture](architecture.md)<br>
### [Installation](installation.md)
