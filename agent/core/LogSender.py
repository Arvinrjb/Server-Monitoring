from pathlib import Path
import requests


def get_offset():
    try:
        with open("offset.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def get_new_logs():
    offset = get_offset()

    with open(
        "agent.log",
        "r",
        encoding="utf-8"
    ) as file:

        file.seek(offset)

        logs = file.readlines()

        new_offset = file.tell()

    return logs, new_offset


def save_offset(offset):
    with open("offset.txt", "w") as file:
        file.write(str(offset))


def parse_logs(logs):
    result = []

    for line in logs:
        try:
            _, level, message = line.split("|", maxsplit=2)

            result.append({
                "level": level.strip(),
                "message": message.strip(),
            })

        except ValueError:
            continue

    return result


def send_logs(url, token):
    logs, new_offset = get_new_logs()

    if not logs:
        return  0

    response = requests.post(
        url,
        headers={
            "X-Agent-Token":token
        },
        json={
            "logs": parse_logs(logs)
        }
    )

    if response.status_code == 201:
        save_offset(new_offset)

