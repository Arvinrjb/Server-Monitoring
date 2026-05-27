from core import ServerMonitorCore
import requests
from time import sleep
import json


def json_convertor(data):
    return json.dumps(data, indent=len(data))



