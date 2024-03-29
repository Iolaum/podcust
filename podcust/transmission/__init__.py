"""

Using the `Linuxserver.io transmission`_ `container image`_

.. _`container image`: https://github.com/linuxserver/docker-transmission
.. _`Linuxserver.io transmission`: https://docs.linuxserver.io/images/docker-transmission

Design Notes:
-------------

- We will be using podman's ability to instantiate containers through a kubernetes yaml file.
- We will use local configuration file to store sensitive information outside of the source code.
  This is security risk and a better option should be implemented for the long term.
- A systemd service is to be created to start the container on boot and close it at power off.
- High level command line commands will be available for common use-cases
  (instantiate container, run it, stop it, upgrade it.)

Maintenance notes:
------------------

Periodically it is good to go through the process of re-creating the kubernetes YAML to see if
there are any important changes we need to make. The process is:

- Stop transmission service
- Stop container
- Create container from linuxserver.io from command line:
- Create new kubernetes yaml file
- Compare with old one.


"""
