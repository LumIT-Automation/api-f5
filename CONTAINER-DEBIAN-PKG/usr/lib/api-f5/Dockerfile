FROM docker.io/amd64/debian:bookworm
LABEL AUTOMATION_CONTAINER_IMAGE="api-f5"
EXPOSE 80/tcp
STOPSIGNAL 37

ADD --chown=0:0 hashicorp-archive-keyring.gpg /
ADD --chown=0:0 hashicorp.list /

ADD PACKAGE /
ADD bootstrap.sh /

RUN ["/bin/bash", "/bootstrap.sh"]
