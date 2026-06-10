from time import sleep
from core.StatusSender import status_sender
from core.logger import logger

logger.info("Server Monitoring Started")

url_ststus = 'http://127.0.0.1:8000/api/agent/status/report/'
url_logs = 'http://127.0.0.1:8000/api/agent/logs/report/'


Token_1 = 'a21f3f3ee4fb31e75c5c59176783f178aa5b4ac5e81b24301fc99219cb2cb875'
Token_2 = 'ab8c13e8947721cf5862b1b7109cc2333f606c4b7ad3b4f5e17b15443b8b5551'


while True: 
    try: 
        request = status_sender(url_ststus, Token_2)
        logger.info(f"Server Status Send, Status Code: {request.status_code} ")
        sleep(10)
    except:
        logger.error("Server Monitoring Error")
        sleep(60)
    


