import platform

from invoke import task

from .config import (
    DOCKER_IMAGE_NAME,
    PACKAGE_VERSION,
)


@task()
def build(context):
    """Build docker image."""
    cmd = f"{get_docker_build_command()} -t {DOCKER_IMAGE_NAME}:{PACKAGE_VERSION} ."
    context.run(cmd)


def get_docker_build_command():
    processor = platform.processor()
    if "arm" in processor:
        print("Build cross platform image")
        return "docker buildx build --platform linux/amd64"
    return "docker build"
