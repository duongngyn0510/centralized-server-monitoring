import os
import requests
import asyncio


NODE_IP = os.getenv('NODE_IP')
HOSTNAME = os.getenv('HOSTNAME')
MONITORING_SERVERS = os.getenv('MONITORING_SERVERS')
NODE_TYPE = os.getenv('NODE_TYPE')

MONITORING_SERVERS = MONITORING_SERVERS.split(' ')

async def test_service(service_name, hostname, port, node_type):
    try:
        _, _ = await asyncio.open_connection(hostname, port)
        print(f"Connected to {service_name} at {hostname}:{port}")
        for monitoring_server in MONITORING_SERVERS:
            try:
                response = requests.post(
                    f"http://{monitoring_server}:8000/add_node", 
                    json={
                            'labels': {'host_gpu': hostname, 'hostname': hostname, 'job': service_name, 'node_type': node_type}, 
                            'targets': [NODE_IP + ':' + str(port)]
                        }
                )
                if response.status_code == 200:
                    print(f"Service {service_name} in host {HOSTNAME} sent to Monitoring service {monitoring_server}")
            except Exception as e:
                print(f"Error sending Node {HOSTNAME} to Monitoring service {monitoring_server}: {e}")

    except ConnectionRefusedError:
        print(f"Connection to {service_name} at {hostname}:{port} refused.")
    except Exception as e:
        print(f"Error connecting to {service_name}: {str(e)}")


async def main():
    services = [
        {"name": "cadvisor", "hostname": HOSTNAME, "port": 8080, "node_type": NODE_TYPE}, # metrics from container
        {"name": "node-exporter", "hostname": HOSTNAME, "port": 9100, "node_type": NODE_TYPE},  # metrics from node
        {"name": "dcgm-exporter", "hostname": HOSTNAME, "port": 9400, "node_type": NODE_TYPE},  # gpu metrics
        {"name": "serving", "hostname": HOSTNAME, "port": 8002, "node_type": NODE_TYPE} # metrics from triton serving
    ]

    tasks = [test_service(service["name"], service["hostname"], service["port"], service['node_type']) for service in services]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())