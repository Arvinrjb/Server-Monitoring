# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

from time import sleep
from core.StatusSender import status_sender
from core.logger import logger
from core.LogSender import send_logs

logger.info("Server Monitoring Started")

status_url = 'http://127.0.0.1:8000/api/agent/status/report/'
logs_url = 'http://127.0.0.1:8000/api/agent/logs/report/'


Token_1 = '105958cf9e5d3f498eb18cf3c4ab9f5bda23c6b0ea096ea4fd5c6232e2d69761'
Token_2 = 'ab8c13e8947721cf5862b1b7109cc2333f606c4b7ad3b4f5e17b15443b8b5551'


while True: 
    try: 
        request = status_sender(status_url, Token_1)
        print(f'status send code: {request.status_code}')
        send_logs(logs_url, Token_1)
        sleep(7)
    except:
        logger.error("Server Monitoring Error, Server connection Error")
        sleep(20)
    


