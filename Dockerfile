FROM espressif/idf

WORKDIR /app
RUN git clone -b v1.16 https://github.com/micropython/micropython.git
WORKDIR /app/micropython
RUN make -C mpy-cross

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

FROM ubuntu:latest
MAINTAINER thebaron88@gmail.com

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install git python3 python3-pip cmake -y

WORKDIR /app/micropython/ports/esp32
RUN make submodules

ENTRYPOINT ["/entrypoint.sh"]
