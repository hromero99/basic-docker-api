from flask import Flask, request
import docker
import json
import psutil

app = Flask(__name__)


def validate_token(token):
    with open("tokens.json", "r") as tokensFile:
        data = json.load(tokensFile)
        if token not in data["tokens"]:
            return False
    tokensFile.close()
    return True


@app.route("/api/v1/images", methods=["GET"])
def get_all_images():
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    docker_client = docker.from_env()
    data = []
    for image_obj in docker_client.images.list(all=True):
        data.append(
            {
                "name": image_obj.tags,
                "id": image_obj.id,
            }
        )
    return data


@app.route("/api/v1/containers", methods=["GET"])
def get_all_containers():
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    docker_client = docker.from_env()
    data = []
    for container_obj in docker_client.containers.list(all=True):
        data.append(
            {
                "name": container_obj.name,
                "id": container_obj.id,
                "image": container_obj.image.id,
                "status": container_obj.status,
            }
        )
    return data


@app.route("/api/v1/containers/<container_id>/restart", methods=["GET"])
def restart_container(container_id):
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    args = request.args.to_dict()
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    docker_client = docker.from_env()
    if "sha256" in container_id:
        container_id = container_id.strip("sha256")
    try:
        docker_container = docker_client.containers.get(container_id.strip(" "))
        docker_container.restart()
        return container_id
    except Exception as error:
        return {"error": f"{error}"}


@app.route("/api/v1/containers/<container_id>/start", methods=["GET"])
def start_container(container_id):
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    args = request.args.to_dict()
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    docker_client = docker.from_env()
    if "sha256" in container_id:
        container_id = container_id.strip("sha256")
    try:
        docker_container = docker_client.containers.get(container_id.strip(" "))
        docker_container.start()
        return container_id
    except Exception as error:
        return {"error": f"{error}"}


@app.route("/api/v1/containers/<container_id>/stop", methods=["GET"])
def stop_container(container_id):
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    args = request.args.to_dict()
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    docker_client = docker.from_env()
    if "sha256" in container_id:
        container_id = container_id.strip("sha256")
    try:
        docker_container = docker_client.containers.get(container_id.strip(" "))
        docker_container.stop()
        return container_id
    except Exception as error:
        return {"error": f"{error}"}


@app.route("/api/v1/containers/<container_id>/remove", methods=["GET"])
def remove_container(container_id):
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    args = request.args.to_dict()
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    docker_client = docker.from_env()
    if "sha256" in container_id:
        container_id = container_id.strip("sha256")
    try:
        docker_container = docker_client.containers.get(container_id.strip(" "))
        docker_container.remove()
        return container_id
    except Exception as error:
        return {"error": f"{error}"}

@app.route("/api/v1/node/cpu",methods=["GET"])
def get_cpu_usage():
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    usage_percenteje_per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    data = {}
    index = 0
    for cpu in usage_percenteje_per_cpu:
        data[index] = cpu
        index = index + 1
    return data

@app.route("/api/v1/node/ram",methods=["GET"])
def get_ram_usage():
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    usage_ram = psutil.virtual_memory()
    data = {
        "used": usage_ram.used,
        "free": usage_ram.free,
        "total": usage_ram.total,
        "percent": (usage_ram.free/usage_ram.total )*100
    }
    return data

@app.route("/api/v1/node/disk",methods=["GET"])
def get_disk_usage():
    if not validate_token(request.headers.get("Authorization")):
        return "Unauthorized"
    usage_principal_disk = psutil.disk_usage('/')
    data = {
        "total": usage_principal_disk.total/10**9,
        "used": usage_principal_disk.used/10**9,
        "free": usage_principal_disk.free/10**9,
        "percent": usage_principal_disk.percent
    }
    return data
    