from invoke import Collection

from . import docker

ns = Collection()
ns.add_collection(docker)
