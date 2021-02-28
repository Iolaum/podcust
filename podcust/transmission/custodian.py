"""
Custodian Class for Transmission container.

Using the `Linuxserver.io transmission`_ `container image`_

.. _`container image`: https://github.com/linuxserver/docker-transmission
.. _`Linuxserver.io transmission`: https://docs.linuxserver.io/images/docker-transmission

This module is responsible for setting up and maintaining the container.

The container is intended to live inside the users home directory, in a hardcoded
location. Namely ``$HOME/transmission/``. The container is deployed within a pod
named transmission.
"""

# from typing import List
from shutil import rmtree
import subprocess
import getpass
from pathlib import Path
import importlib.resources as pkg_resources
from podcust.tools import get_user_input


class TransmissionCust:
    """
    Main class for handling the transmission container.

    :param name: The full repository name of the image this class is custodian for.
    """

    name: str
    image_id: str
    username: str

    def __init__(self, name: str = "ghcr.io/linuxserver/transmission"):
        """
        Initialize TransmissionCust class.
        """
        self.name = name
        self.image_id = ""
        self.username = getpass.getuser()

    def pull_latest_transmission_image(self):
        """
        Pull latest transmission container image from linuxserver.io

        The relevant shell command is::

        $ podman pull ghcr.io/linuxserver/transmission

        """

        command_text = "podman pull $name"
        command_text = command_text.replace("$name", self.name)

        try:
            p = subprocess.run(
                command_text,
                text=True,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            print(p.stdout)

        except Exception as e:
            print(e)

    def deploy(self):
        """
        Create a pod named transmission to deploy our container.
        For a successful deployment the following steps must take place:

        - Create the necessary folders, and give them proper permissions.
        - Write the proper kube yaml file that we 'll use to deploy the container.
        """

        # Let's create master path where we 'll put the container
        main_path: Path = Path.home().joinpath("transmission")

        # Let's delete everything allready present on the space we want to use:
        rmtree(main_path)

        # let's recreate the directory now
        main_path.mkdir()
        # let's create additional needed directories
        main_path.joinpath("config").mkdir()
        main_path.joinpath("watch").mkdir()
        main_path.joinpath("downloads").mkdir()

        # read package file
        # https://stackoverflow.com/a/20885799/1904901
        # To access a file inside the current module, set the package argument to __package__,
        yaml_template = pkg_resources.read_text(
            __package__, "transmission-kube-template.yml"
        )

        # populate template with proper entries:
        usnmae = get_user_input("Enter transmission username:")
        yaml_template = yaml_template.replace("$SET_USER", usnmae)
        password = get_user_input("Enter transmission password:")
        yaml_template = yaml_template.replace("$SET_PASSWD", password)
        yaml_template = yaml_template.replace("$LOCAL_USER", self.username)

        # write kubernetes template
        main_path.joinpath("transmission-kube.yml").write_text(yaml_template)

        print(yaml_template)
