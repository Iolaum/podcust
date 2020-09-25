"""Console script for podcust.

Useful documentation at:
https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
https://click.palletsprojects.com/en/7.x/complex/
"""

import click
from podcust.demo.custodian import DemoCust


@click.group()
def main(args=None):
    """Podcust commands provide a wrapper around lower level utilities
    from podman, the Operating System and the container you are managing."""
    click.echo("Welcome to Podman Custodian!")


@click.group()
@click.pass_context
def demo(ctx):
    """Podcust tools for demo container image."""
    # We can only use ctx.obj to create and share between commands.
    ctx.obj = DemoCust()
    click.echo("Initializing Podman Custodian Demo class.")


@click.command()
@click.pass_obj
def rmi(obj):
    """Remove a demo image."""
    click.echo("Removing Demo image.")
    obj.remove_stored_image()
    click.echo("Image removed!")


@click.command()
@click.pass_obj
def rmec(obj):
    """Remove an exited demo container."""
    click.echo("Removing Demo containers.")
    obj.removed_exited_containers()
    click.echo("Containers removed!")


main.add_command(demo)
demo.add_command(rmi)
demo.add_command(rmec)
