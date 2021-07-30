#!/bin/bash
docker run -it --name micropython --rm --mount type=bind,source=${PWD}/quickled,target=/usercmodule/quickled --device=/dev/ttyUSB0 micropython /bin/bash
