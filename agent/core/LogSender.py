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



# def read_logs():

#     path = Path("agent.log")

#     if not path.exists():
#         return []

#     with open(
#         "agent.log",
#         "r",
#         encoding="utf-8"
#     ) as file:

#         return file.readlines()
    


def send_logs(url, token):
    logs, new_offset = get_new_logs()

    if not logs:
        return

    response = requests.post(
        url,
        headers={
            "X-Agent-Token":token
        },
        json={
            "message": "".join(logs)
        }
    )

    if response.status_code == 201:
        save_offset(new_offset)


# def send_logs(url, token):

#     logs = read_logs()
#     if not logs:
#         return

#     requests.put(
#         url,
#         headers={
#             "X-Agent-Token": token
#         },
#         json={
#             "logs": logs
#         }
#     )
# send_logs()