FROM fedora:latest

RUN dnf -y install python3-flask

RUN mkdir /app
COPY ./hello.py /app/

RUN cd /app
# Command that gets run when the container is started.
CMD python3 /app/hello.py
