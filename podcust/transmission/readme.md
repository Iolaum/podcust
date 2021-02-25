# Transmission Container Image

We will be using the [transmission](https://transmissionbt.com/about/) [docker container image](https://github.com/linuxserver/docker-transmission) from linuxserver.io [documented here](https://docs.linuxserver.io/images/docker-transmission). We will be using that image with podman.

## Design Notes.

- We will be using podman's ability to instantiate containers through a kubernetes yaml file.
- We will use local configuration file to store sensitive information outside of the source code.
  This is security risk and a better option should be implemented for the long term.
- A systemd service is to be created to start the container on boot and close it at power off.
- High level command line commands will be available for common use-cases (instantiate container, run it, stop it, upgrade it.)
