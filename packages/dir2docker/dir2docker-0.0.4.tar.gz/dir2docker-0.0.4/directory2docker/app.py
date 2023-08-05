import docker

from pathlib import Path
from tokenize import String
from traitlets import Any, Dict, Int, List, Unicode, Bool, default
from traitlets.config import Application

# def create_requirements_file():


# def create_docker_file():


# def execute_docker_build():


class Directory2Docker(Application):
    """An application for converting working directories to docker images"""

    def push_docker(
        registry: String, image_name: String, username: String, password: String
    ):
        """Build image.
        Arguments:
            registry(String): Name of the docker repository to push to.
            image_name(String): Name of the created docker image
            repo_creds_file(Path): path to credentials file to push to public repos
            username(String): Username for docker login
            password(String): Password for docker login
        """
        client = docker.from_env()
        client.login(username=username, password=password, registry=registry)
        client.images.push(image_name, stream=True, decode=True)
        return "success"
