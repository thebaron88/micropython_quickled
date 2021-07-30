docker run -it --name micropython --rm --mount type=bind,source=%~dp0\quickled,target=/usercmodule/quickled micropython /bin/bash
