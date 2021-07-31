# New Build Guide
This is the guide on how to build under remote dev.

## Set up dev container
`docker run -it --name code-server -p 8080:8080 -v "$HOME/.config:/home/coder/.config" -v "project:/home/coder/project" -u "$(id -u):$(id -g)" -v /var/run/docker.sock:/var/run/docker.sock -e "DOCKER_USER=$USER" codercom/code-server:latest`

Passing through the docker socket enables us to use docker commands in the dev machine.
Once the machine has booter then goto `http://baron-desktop.lan:8080/?folder=/home/coder/project`

On that machine we then need docker

`curl -fsSL https://get.docker.com -o get-docker.sh`
`sh ./get-docker.sh`

And we need to check out our source code into the continer. This required me to chown it the first time around. Not sure why.
Then to build we need to fire up the docker image:

`docker run -it --name micropython --rm -v "project:/usercmodule/quickled" micropython /bin/bash`

And compile

`make BOARD=GENERIC_OTA USER_C_MODULES=/usercmodule/quickled/quickled/quickled/micropython.cmake`

## Flash version
SET PATH=C:\Users\Mark\AppData\Local\Programs\Python\Python39;C:\Users\Mark\AppData\Local\Programs\Python\Python39\Scripts;%PATH%
esptool.py.exe --before no_reset erase_flash
esptool.py.exe --chip esp32 --port COM3 -b 921600 write_flash -z 0x1000 firmware.bin
