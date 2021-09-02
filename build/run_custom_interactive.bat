docker run -it --name micropython -d --rm --mount type=bind,source=%~dp0\..,target=/github/workspace --entrypoint /bin/bash micropython

docker cp ../GENERIC_OTA_LED micropython:/app/micropython/ports/esp32/boards/GENERIC_OTA_LED
docker exec -ti micropython sh -c ". $IDF_PATH/export.sh && make BOARD=GENERIC_OTA_LED USER_C_MODULES=/github/workspace/quickled/micropython.cmake"
docker cp micropython:/app/micropython/ports/esp32/build-GENERIC_OTA_LED/bootloader/bootloader.bin ..
docker cp micropython:/app/micropython/ports/esp32/build-GENERIC_OTA_LED/partition_table/partition-table.bin  ..
docker cp micropython:/app/micropython/ports/esp32/build-GENERIC_OTA_LED/ota_data_initial.bin  ..
docker cp micropython:/app/micropython/ports/esp32/build-GENERIC_OTA_LED/micropython.bin ..

docker exec -ti micropython sh -c "cd /github/workspace/build && python /github/workspace/build/makefs.py"

%LOCALAPPDATA%\Programs\Python\Python39\Scripts\esptool.exe -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 ..\bootloader.bin 0x8000 ..\partition-table.bin 0xd000 ..\ota_data_initial.bin 0x10000 ..\micropython.bin 0x310000 ..\fs.bin
docker stop micropython 