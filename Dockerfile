FROM fedora:32

RUN dnf -y update
RUN dnf -y install python3-pip python3-tox make git findutils
RUN dnf clean all

RUN git clone https://github.com/Iolaum/podcust.git /src
RUN cd /src && pip install --upgrade pip && pip install .[dev] --use-feature=2020-resolver
RUN chmod +x /src/entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]