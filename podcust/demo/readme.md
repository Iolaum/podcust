Information on the podman build command can be found [here](https://podman.readthedocs.io/en/latest/markdown/podman-build.1.html).

Build container:

```
# We start from within the demo folder as our working directory.
# running drom cached results:
$ podman build -f Dockerfile -t flask_demo
STEP 1: FROM fedora:latest
STEP 2: RUN dnf -y install python3-flask
--> Using cache fa023a477b248cd2978c7f6ab9aa0a7b8859fcad6a9323e99bf989b6942ed38c
STEP 3: RUN mkdir /app
--> Using cache 52358f5a145e01a182d3a5a687e17a8e1e42e6127cbf726fbe3e06bdb889387d
STEP 4: COPY ./hello.py /app/
--> Using cache fc56d9d6a012828c94d25ab430d56ca6b7bac02573bdabb0602649a476778b39
STEP 5: RUN cd /app
--> Using cache b74ff97fbf07d4c8f10b0891babf0aac526a73dfdb7f9bc82ba038cdeb8a3ec5
STEP 6: CMD python3 /app/hello.py
STEP 7: COMMIT flask_demo
--> b314df57b99
b314df57b99ff450845b873d0ae140f7b1385f1dd06022b3927ece12bfbb3e41
$ podman run -p 5000:5000 localhost/flask_demo
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [19/Sep/2020 21:11:36] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [19/Sep/2020 21:11:53] "GET / HTTP/1.1" 200 -
^C
```

After we stop the container we have:

```
$ podman image ls
REPOSITORY                         TAG     IMAGE ID      CREATED         SIZE
localhost/flask_demo               latest  b314df57b99f  12 minutes ago  458 MB
registry.fedoraproject.org/fedora  latest  00ff39a8bf19  2 months ago    189 MB
$ podman ps
CONTAINER ID  IMAGE   COMMAND  CREATED  STATUS  PORTS   NAMES
$ 
```

We can remove an image with `podman image rm` and by adding the `-f` option if needed.