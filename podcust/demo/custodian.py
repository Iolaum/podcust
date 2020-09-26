"""
Custodian Class for Demo container.
"""

from typing import List
import subprocess
from pathlib import Path, PurePath


class DemoCust:
    """
    Main class for handling the httpdemo container.

    The httpdemo container just spawns an a container with an apache web server
    service serving the Fedora Test page through http.

    :param name: The Repository name of the image this class is custodian for.
    """

    name: str
    image_id: str

    def __init__(self, name: str = "localhost/httpdemo"):
        """
        Initialize DemoCust class.
        """
        self.name = name
        self.image_id = ""

    def find_stored_image_id(self) -> List[str]:
        """
        This function looks if the system has an appropriate container image and
        returns the id of that image.

        Current implementation assumes that the first match is the one we are after.

        TODO: Specify what tag we want to match?
        """

        image_id_list: List[str] = []
        check = subprocess.run(
            "podman images",
            text=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # split results line by line and remove all but one whitespace
        processed_lines = []
        for line in check.stdout.splitlines():
            # default split separator is spaces, too many spaces act as one separator
            tmp = " ".join(line.split())
            processed_lines.append(tmp.split(" "))

        # We expect the first line to have the columns below:
        # ['REPOSITORY', 'TAG', 'IMAGE', 'ID', 'CREATED', 'SIZE']
        for il in processed_lines:
            if il[0] == self.name:
                image_id_list.append(il[2])

        return image_id_list

    def remove_stored_image(self):
        """
        Removes a stored container image corresponding to the name
        the class has been instantiated to.
        """

        image_id_list = self.find_stored_image_id()
        command_text = "podman image rm $image_id"

        for iid in image_id_list:
            command_text = command_text.replace("$image_id", iid)
            print(f"Removing image {self.name} with image id {iid}")
            try:
                subprocess.run(
                    command_text,
                    text=True,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )
            except Exception as e:
                print(e)

    def find_exited_containers(self):  # noqa: E501
        """
        Find all containers of demo type that have run and exited.

        You can see here a sample output of the command we use to find the containers we want
        to remove:  # noqa: E501
        $ podman ps -a
        CONTAINER ID  IMAGE                                     COMMAND     CREATED     STATUS                   PORTS                 NAMES
        1b5fe6643ece  localhost/httpdemo:latest                 /sbin/init  2 days ago  Exited (0) 2 days ago    0.0.0.0:8080->80/tcp  strange_wu
        3ea6bf480c47  localhost/httpdemo:latest                 /bin/bash   2 days ago  Exited (0) 2 days ago    0.0.0.0:8080->80/tcp  funny_williams
        63604b048bc9  registry.fedoraproject.org/fedora:latest  /bin/bash   2 days ago  Exited (0) 2 days ago                          practical_kowalevski
        b3e4d5b363ce  localhost/httpdemo:latest                 /sbin/init  2 days ago  Exited (137) 2 days ago  0.0.0.0:8080->80/tcp  pedantic_tesla
        c4e4a6847c3d  localhost/httpdemo:latest                 /bin/bash   2 days ago  Exited (0) 2 days ago    0.0.0.0:8080->80/tcp  jolly_volhard
        dc9bffeef1c2  registry.fedoraproject.org/fedora:latest  /bin/bash   2 days ago  Exited (0) 2 days ago    0.0.0.0:8080->80/tcp  zealous_blackburn0
        """

        container_id_list: List[str] = []
        check = subprocess.run(
            "podman ps -a",
            text=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        # split results line by line and remove all but one whitespace
        processed_lines = []
        for line in check.stdout.splitlines():
            # default split separator is spaces, too many spaces act as one separator
            tmp = " ".join(line.split())
            processed_lines.append(tmp.split(" "))

        # We expect the first line to have the columns below:
        # ['CONTAINER ID', 'IMAGE', 'COMMAND', 'CREATED', 'CREATED', 'STATUS', 'PORTS', 'NAMES']
        for il in processed_lines:
            container_name = il[1].split(":")[0]
            status = il[6]

            if container_name == self.name and status == "Exited":
                container_id_list.append(il[0])

        return container_id_list

    def removed_exited_containers(self):
        """
        Remove all containers of demo type that have run and exited.

        Remove an image with:
        podman container rm 3ea6bf480c47
        """

        container_id_list = self.find_exited_containers()

        for cont in container_id_list:

            try:
                print(f"Removing container {self.name} with container id {cont}")
                command_text = "podman container rm $container_id"
                command_text = command_text.replace("$container_id", cont)
                subprocess.run(
                    command_text,
                    text=True,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )

            except Exception as e:
                print(e)

    def build_demo_image(self):
        """
        Build an image for the demo container. Use the dockerfile located at this folder.

        The command to build a container is:
        podman build -f Dockerfile -t httpdemo
        """

        command_text = "podman build -f $dockerfile -t httpdemo"
        dockerfile_dir = str(
            PurePath.joinpath(Path(__file__).parent, "Dockerfile")
        )
        command_text = command_text.replace("$dockerfile", dockerfile_dir)

        try:
            subprocess.run(
                command_text,
                text=True,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

        except Exception as e:
            print(e)
