from time import sleep
from core.StatusSender import status_sender
from core.logger import logger
from core.LogSender import send_logs

logger.info("Server Monitoring Started")

status_url = 'http://127.0.0.1:8000/api/agent/status/report/'
logs_url = 'http://127.0.0.1:8000/api/agent/logs/report/'


Token_1 = '182c25a06d6c81a2f79b34e64e13a1a10d362b62a1e87ad986a47908fe2dace2'
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
    


