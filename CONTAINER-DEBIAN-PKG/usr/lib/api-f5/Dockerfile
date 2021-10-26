FROM docker.io/amd64/debian:buster
LABEL AUTOMATION_CONTAINER_IMAGE="api-f5"
EXPOSE 80/tcp

ADD PACKAGE /
ADD bootstrap.sh /

RUN ["/bin/bash", "/bootstrap.sh"]
