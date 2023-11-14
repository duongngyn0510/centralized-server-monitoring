import os

import requests
from dotenv import dotenv_values

config = dotenv_values("node-gpu/.env")

NODE_IP = os.getenv("NODE_IP")
HOSTNAME = os.getenv("HOSTNAME")
MONITORING_SERVERS = config["MONITORING_SERVERS"]
MONITORING_SERVERS = MONITORING_SERVERS.split(" ")

for monitoring_server in MONITORING_SERVERS:
    try:
        response = requests.post(
            f"http://{monitoring_server}:8000/remove_node", json={"ip": NODE_IP}
        )
        if response.status_code == 200:
            print(
                f"Node IP of {HOSTNAME} sent to Monitoring service {monitoring_server}"
            )

    except Exception as e:
        print(
            f"Error sending Node {HOSTNAME} to Monitoring service {monitoring_server}: {e}"
        )
