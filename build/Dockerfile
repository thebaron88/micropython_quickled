FROM espressif/idf:release-v4.2

WORKDIR /app
RUN git clone -b v1.16 https://github.com/micropython/micropython.git

WORKDIR /app/micropython
RUN make -C mpy-cross

WORKDIR /app/micropython/ports/esp32
RUN make submodules

RUN pip install littlefs-python

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
