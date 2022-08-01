import os
import sys

MODE = os.environ.get("MODE")


def docker_setup():

    create_folder_if_none("static")

    create_folder_if_none("staticfiles")

    os.system("docker compose build web")
    
    os.system("docker compose run web ./manage.py check")

    os.system("docker compose run web ./manage.py migrate")

    os.system("docker compose run web ./manage.py collectstatic --noinput")

    os.system("docker container prune")

    os.system("docker compose up -d web")

    os.system("docker compose logs -f web")


def pipenv_setup():
    create_folder_if_none("static")
    create_folder_if_none("staticfiles")
    os.system("pipenv shell")


def create_folder_if_none(newpath: str) -> bool:
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        return True
    return False


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


if MODE == "docker":
    if is_tool("docker"):
        docker_setup()
elif MODE == "pipenv":
    if sys.version_info < (3, 10):
        print("Please upgrade your Python version to 3.10.0 or higher")
        sys.exit()
    if not is_tool(MODE):
        print("Virtual environment tools necesary not could not be found")
        sys.exit()

    pipenv_setup()

else:
    print("Please specify the mode of operation")
    sys.exit()
