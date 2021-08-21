FROM docker.io/amd64/debian:buster
EXPOSE 80/tcp

ADD PACKAGE /
ADD bootstrap.sh /

RUN ["/bin/bash", "/bootstrap.sh"]
