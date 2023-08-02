from flask import Flask,request
import docker
import json
app = Flask(__name__)

def validate_token(token):
    with open("tokens.json",'r') as tokensFile:
        data = json.load(tokensFile)
        if token not in data["tokens"]:
            return False
    tokensFile.close()
    return True


@app.route("/api/v1/images",methods=["GET"])
def get_all_images():
    if not validate_token(request.headers.get('Authorization')):
        return "Unauthorized"
    docker_client = docker.from_env()
    data = []
    for image_obj in docker_client.images.list(all=True):
        data.append({
            "name": image_obj.tags,
            "id": image_obj.id,
        })
    return data

@app.route("/api/v1/containers",methods=["GET"])
def get_all_containers():
    if not validate_token(request.headers.get('Authorization')):
        return "Unauthorized"
    docker_client = docker.from_env()
    data = []
    for container_obj in docker_client.containers.list(all=True):
        data.append({
            "name": container_obj.name,
            "id": container_obj.id,
            "image": container_obj.image.id,
            "status": container_obj.status
        })
    return data