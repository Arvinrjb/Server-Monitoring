from pathlib import Path
import requests


def read_logs():

    path = Path("agent.log")

    if not path.exists():
        return []

    with open(
        "agent.log",
        "r",
        encoding="utf-8"
    ) as file:

        return file.readlines()
    

def send_logs(url, token):

    logs = read_logs()

    if not logs:
        return

    requests.post(
        url,
        headers={
            "X-Agent-Token": token
        },
        json={
            "logs": logs
        }
    )