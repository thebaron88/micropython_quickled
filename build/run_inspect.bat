docker run -it --name micropython --rm --mount type=bind,source=%~dp0\..,target=/github/workspace --entrypoint /bin/bash micropython
