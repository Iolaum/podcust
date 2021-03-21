"""
Systemd utilities to create services for Podman Custodian Transmission module.

The systemd user unit service performs two actions.

- Upon boot (user default.target) the pod starts and updates itself if a new version is present.
- Upon shutdown (execstop) the pod stops (to be started on next boot)

The update process is tied to the system boot for simplicity. This is to piggyback
on expected system reboots after host (rpm-ostree) updates.
"""

from pathlib import Path
from pwd import getpwuid
from os import getuid
from subprocess import run
import importlib.resources as pkg_resources


def create_service_unit():
    """
    Create a systemd user unit for podman cutodian's transmission module.
    Use predefined template and modify where needed.

    We want the service to run when the user logs out so that all the changes
    they made are fixed if needed. We consult the following sources
    to create the appropriate systemd service template:

    * https://wiki.archlinux.org/index.php/Systemd/User
    * https://superuser.com/questions/1037466/
      how-to-start-a-systemd-service-after-user-login-and-stop-it-before-user-logout/1269158
    * https://askubuntu.com/questions/293312/
      execute-a-script-upon-logout-reboot-shutdown-in-ubuntu/796157#796157

    We want to add a systemd user unit to run transmission-pod on certain times. In order to do
    this we want to crete a unit at a proper location. According to:
    https://wiki.archlinux.org/index.php/Systemd/User
    our options are:

    * /usr/lib/systemd/user/:

      where units provided by installed packages belong.
    * ~/.local/share/systemd/user/

      where units of packages that have been installed in the home directory belong.
    * /etc/systemd/user/

      where system-wide user units are placed by the system administrator.
    * ~/.config/systemd/user/

      where the user puts their own units.

    The latter choice only works when a user is logged in! Hence we use
    ``/etc/sysyemd/user/`` so that the process starts and stops at boot.
    """

    # create unit in a location we don't need admin access first!
    # we 'll copy it afterwards to minimise use cases where we need root access :(
    tmp_path = Path.home().joinpath("transmission").joinpath("transmission-pod.service")
    unit_path = Path("/etc/sysyemd/user/").joinpath("transmission-pod.service")

    # read package file
    # https://stackoverflow.com/a/20885799/1904901
    # To access a file inside the current module, set the package argument to __package__,
    template = pkg_resources.read_text(__package__, "transmission-pod.service")
    # we want the service to run as a user service!
    cuser = getpwuid(getuid()).pw_name
    template = template.replace("$set_user", cuser)

    tmp_path.write_text(template)
    # copy service unit file to final location
    run(f"sudo cp {tmp_path} {unit_path}")

    print("Systemd user service unit installed!")


def activate_service():
    """
    After a transmission-pod setup is run we need to activate the service we installed.
    """

    run(["systemctl", "--user", "enable", "transmission-pod"], check=True)
    run(["systemctl", "--user", "start", "transmission-pod"], check=True)


def deactivate_service():
    """
    Deactivate a running transmission-pod service.
    """

    run(["systemctl", "--user", "stop", "transmission-pod"], check=True)
    run(["systemctl", "--user", "disable", "transmission-pod"], check=True)


def delete_service_unit():
    """
    Delete the systemd user unit for podman cutodian's transmission module.
    """

    # get expected unit's location:
    unit_path = Path("/etc/sysyemd/user/").joinpath("transmission-pod.service")
    unit_path.unlink()
    print("systemd user unit for podman cutodian's transmission module deleted")
