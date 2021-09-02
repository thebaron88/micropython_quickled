docker run -it --name micropython --rm --mount type=bind,source=%~dp0\..,target=/github/workspace micropython GENERIC_OTA_LED 120 /github/workspace/quickled/micropython.cmake
