/home/baron/esp/esp-idf/components/esptool_py/esptool/esptool.py -b 460800 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 ../bootloader.bin 0x8000 ../partition-table.bin 0xd000 ../ota_data_initial.bin 0x10000 ../micropython.bin  0x310000 ../python_boot.bin

baron@baron-laptop:~/build-GENERIC_OTA_LED/build-GENERIC_OTA_LED$ /home/baron/esp/esp-idf/components/esptool_py/esptool/esptool.py -b 460800 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 ./bootloader/bootloader.bin 0x8000 ./partition_table/partition-table.bin 0xd000 ./ota_data_initial.bin 0x10000 ./micropython.bin  0x310000 ~/micropython_quickled_desktop/python_boot.bin

