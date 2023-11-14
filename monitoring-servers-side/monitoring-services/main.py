import yaml
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel


class Node(BaseModel):
    labels: dict  # job and hostname
    targets: list  # list services (in my yaml style, targets have only one service)


class NodeIP(BaseModel):
    ip: str


CONFIG_FILE = "shared_data/targets.yaml"


def add_node_config_file(new_node: Node):
    targets = new_node.targets[0]
    with open(CONFIG_FILE, encoding="utf-8") as f:
        node_data = yaml.safe_load(f)

    if isinstance(node_data, list):
        # Services already exist in the target file
        existed_node_services = set(
            [node_service["targets"][0] for node_service in node_data]
        )
        if targets not in existed_node_services:
            with open(CONFIG_FILE, mode="a", encoding="utf-8") as f:
                yaml.dump([new_node.dict()], f)

            logger.debug(
                f"Save node: {new_node.labels['hostname']} with service {new_node.labels['job']} at {targets} sucessfully !"
            )
        else:
            logger.debug(
                f"Node: {new_node.labels['hostname']} with service {new_node.labels['job']} at {targets} already exists !"
            )

    else:
        # No services in the target file
        logger.debug("No services found in the target file")
        with open(CONFIG_FILE, mode="a", encoding="utf-8") as f:
            yaml.dump([new_node.dict()], f)
        logger.debug(
            f"Save node: {new_node.labels['hostname']} with service {new_node.labels['job']} at {targets} sucessfully !"
        )


def remove_node_config_file(node_ip: NodeIP):
    with open(CONFIG_FILE, encoding="utf-8") as f:
        node_data = yaml.safe_load(f)

    if node_data:
        existed_node_ip = set(
            [node_service["targets"][0].split(":")[0] for node_service in node_data]
        )
        if node_ip in existed_node_ip:
            new_node_data = [
                node_service
                for node_service in node_data
                if not any(
                    node_ip in target for target in node_service.get("targets", [])
                )
            ]
            if new_node_data:  # Nodes still exist
                with open(CONFIG_FILE, mode="w", encoding="utf-8") as f:
                    yaml.dump(new_node_data, f)
            else:  # No nodes exist anymore
                with open(CONFIG_FILE, mode="w", encoding="utf-8") as f:
                    f.write("")
            logger.debug(f"Node {node_ip} removed sucessfully !")
        else:
            logger.debug(f"Node {node_ip} does not exist !")
    else:
        logger.debug(f"No nodes exist !")


app = FastAPI()


@app.post("/add_node")
async def add_node(new_node: Node):
    if new_node:
        add_node_config_file(new_node)
        return {"message": "Node update received"}
    else:
        raise HTTPException(status_code=400, detail="Invalid Node update data")


@app.post("/remove_node")
async def remove_node(node: NodeIP):
    node_ip = node.ip
    if node_ip:
        remove_node_config_file(node_ip)
        return {"message": "Node update received"}
    else:
        raise HTTPException(status_code=400, detail="Invalid Node update data")
