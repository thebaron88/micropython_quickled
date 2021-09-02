docker run -it --name micropython -d --rm --mount type=bind,source=%~dp0\..,target=/github/workspace --entrypoint /bin/bash micropython

docker exec -ti micropython sh -c "pip install littlefs-python"
docker exec -ti micropython sh -c "python /github/workspace/build/makefs.py --dir /github/workspace/python --out /github/workspace/fs2.bin --block_count 120"
docker exec -ti micropython sh -c "gzip -9 -k -f /github/workspace/fs2.bin"

docker stop micropython 