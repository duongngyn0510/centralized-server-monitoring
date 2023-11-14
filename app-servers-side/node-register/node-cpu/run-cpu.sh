NODE_IP=$(hostname -I | awk '{print $1}') HOSTNAME=$(hostname) docker compose -f node-cpu/docker-compose-cpu.yaml up --build -d
