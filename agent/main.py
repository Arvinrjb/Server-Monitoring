# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from time import sleep
from core.StatusSender import status_sender
from core.logger import logger
from core.LogSender import send_logs

logger.info("Server Monitoring Started")

BASE_URL = "http://127.0.0.1:8000"
STATUS_URL = f"{BASE_URL}/api/agent/status/report/"
LOGS_URL = f"{BASE_URL}/api/agent/logs/report/"
TOKEN = '105958cf9e5d3f498eb18cf3c4ab9f5bda23c6b0ea096ea4fd5c6232e2d69761'


while True: 
    try: 
        request = status_sender(STATUS_URL, TOKEN)
        print(f'status send code: {request.status_code}')
        send_logs(LOGS_URL, TOKEN)
        sleep(7)
    except:
        logger.error("Server Monitoring Error, Server connection Error")
        sleep(20)
    


