Information on the podman build command can be found [here](https://podman.readthedocs.io/en/latest/markdown/podman-build.1.html).

Build container:

```
# We start from within the demo folder as our working directory.
# running drom cached results:
$ podman build -f Dockerfile -t httpdemo
STEP 1: FROM fedora
STEP 2: RUN dnf update -y
--> Using cache 10b6af0f1de0f9a5a117995909254240b24bc7015a0eaed673ba0b2a85055d80
STEP 3: RUN dnf -y install httpd
--> Using cache 6b1665be9f74b21badd044f747ffc6f30f2efb855f185ba59a145eeb851d6ed7
STEP 4: RUN dnf clean all
--> Using cache 13993f862bc4bb8b7aad2e27c188d07314f65b61722b8948f00018bb0a90126f
STEP 5: EXPOSE 80
--> Using cache d2728e16a717b5445e09138b0a8c31be7873514e70f18eff5414166cf5a21aea
STEP 6: CMD [ "/sbin/init" ]
STEP 7: COMMIT httpdemo
--> 5ff443b5499
5ff443b54997e01588961b9047860a5865b46ac6f92aeafcc415a0c0fa5e13ec
# -d starts the container in the background
$ podman run -d -p 8080:80 localhost/httpdemo
b3e4d5b363cebe1df9c4027416be15aa95cdcd30d3acd7e79b8beb3387e1f90b
$ podman ps
CONTAINER ID  IMAGE                      COMMAND     CREATED        STATUS            PORTS                 NAMES
b3e4d5b363ce  localhost/httpdemo:latest  /sbin/init  7 seconds ago  Up 6 seconds ago  0.0.0.0:8080->80/tcp  pedantic_tesla
$ podman exec b3e4d5b363ce systemctl start httpd
# Fedora Webserver Test server page appears at localhost:8080
$ podman exec b3e4d5b363ce systemctl status httpd
● httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
     Active: active (running) since Tue 2020-09-22 20:11:25 UTC; 1min 14s ago
       Docs: man:httpd.service(8)
   Main PID: 27 (httpd)
     Status: "Total requests: 3; Idle/Busy workers 100/0;Requests/sec: 0.0435; Bytes served/sec: 146 B/sec"
      Tasks: 213 (limit: 307)
        CPU: 134ms
     CGroup: /system.slice/httpd.service
             ├─27 /usr/sbin/httpd -DFOREGROUND
             ├─28 /usr/sbin/httpd -DFOREGROUND
             ├─29 /usr/sbin/httpd -DFOREGROUND
             ├─30 /usr/sbin/httpd -DFOREGROUND
             └─31 /usr/sbin/httpd -DFOREGROUND

Sep 22 20:11:25 b3e4d5b363ce systemd[1]: Starting The Apache HTTP Server...
Sep 22 20:11:25 b3e4d5b363ce httpd[27]: AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 10.0.2.100. Set the 'ServerName' directive globally to suppress this message
Sep 22 20:11:25 b3e4d5b363ce httpd[27]: Server configured, listening on: port 80
Sep 22 20:11:25 b3e4d5b363ce systemd[1]: Started The Apache HTTP Server.
$ podman exec b3e4d5b363ce systemctl stop httpd
$ podman kill b3e4d5b363ce

```

After we stop the container we have:

```
$ podman images
REPOSITORY                         TAG     IMAGE ID      CREATED        SIZE
localhost/httpdemo                 latest  5ff443b54997  5 minutes ago  582 MB
registry.fedoraproject.org/fedora  latest  00ff39a8bf19  2 months ago   189 MB
$ podman ps
CONTAINER ID  IMAGE   COMMAND  CREATED  STATUS  PORTS   NAMES
$ 
```

We can remove an image with `podman image rm` and by adding the `-f` option if needed.


Some additional tips are:

```
# Get a shell inside the container: (i:interactiive, t:tty)
$ podman exec -it dd4392d012be30830e6ad347bbe555428a30ffffc9ab403e62e740ea55ab9708 /bin/bash
```

Notes (TODO) on the demo custodian class functionality:
- Build the container
- Identify appropriate image of the container's type
- Run an existing image in the background
- Start and stop services (functionality) inside the container.
- Functionality checks (Fetch webpage)
