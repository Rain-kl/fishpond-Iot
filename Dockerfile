FROM ubuntu:latest
LABEL authors="ryan"

ENTRYPOINT ["top", "-b"]