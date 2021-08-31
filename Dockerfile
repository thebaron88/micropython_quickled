FROM ubuntu:latest
MAINTAINER thebaron88@gmail.com

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install git python3 python3-pip cmake -y

WORKDIR /app
RUN git clone -b v4.0.2 --recursive https://github.com/espressif/esp-idf.git
RUN git clone -b v1.16 https://github.com/micropython/micropython.git

WORKDIR /app/esp-idf
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ./install.sh
RUN /usr/bin/python -m pip install --user -r /app/esp-idf/requirements.txt

WORKDIR /app/micropython
RUN make -C mpy-cross

ENV IDF_PATH=/app/esp-idf
ENV IDF_TOOLS_PATH=/root/.espressif/tools
ENV PATH="${IDF_PATH}/tools:${IDF_TOOLS_PATH}/xtensa-esp32-elf/esp-2020r3-8.4.0/xtensa-esp32-elf/bin:${PATH}"

WORKDIR /app/micropython/ports/esp32
RUN make submodules
#RUN make BOARD=GENERIC_OTA USER_C_MODULES=/usercmodule/quickled/micropython.cmake
ENTRYPOINT ["/entrypoint.sh"]
