from flask import Flask, request
import docker
import json

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
def restart_container(container_id):
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
def restart_container(container_id):
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
def restart_container(container_id):
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
