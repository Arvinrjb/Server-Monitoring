import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

try:
    handler = RotatingFileHandler(
    "agent.log",
    maxBytes=1024 * 1024,
    backupCount=3
    )
except:
    pass


logger = logging.getLogger("agent")
