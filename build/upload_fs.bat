docker run -it --name micropython -d --rm --mount type=bind,source=%~dp0\..,target=/github/workspace --entrypoint /bin/bash micropython

docker exec -ti micropython sh -c "pip install littlefs-python"
docker exec -ti micropython sh -c "python /github/workspace/build/makefs.py --dir /github/workspace/python_boot --out /github/workspace/python_boot.bin --block_count 120"
docker exec -ti micropython sh -c "gzip -9 -k -f /github/workspace/python_boot.bin"
docker exec -ti micropython sh -c "python /github/workspace/build/makefs.py --dir /github/workspace/python --out /github/workspace/python.bin --block_count 120"
docker exec -ti micropython sh -c "gzip -9 -k -f /github/workspace/python.bin"

docker stop micropython 

%LOCALAPPDATA%\Programs\Python\Python39\Scripts\esptool.py.exe -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x310000 ..\python_boot.bin
%USERPROFILE%\Downloads\putty.exe -load "mpy"