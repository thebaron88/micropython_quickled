#!/usr/bin/env bash
set -e

. $IDF_PATH/export.sh

if [ ! -d "/app/micropython/ports/esp32/boards/$1" ]; then
  cp -r /github/workspace/boards/$1 /app/micropython/ports/esp32/boards/$1
fi

cd /app/micropython/ports/esp32
make BOARD=$1 USER_C_MODULES=$3

gzip -9 -k /app/micropython/ports/esp32/build-$1/bootloader/bootloader.bin
cp /app/micropython/ports/esp32/build-$1/bootloader/bootloader.bin /github/workspace/bootloader.bin
cp /app/micropython/ports/esp32/build-$1/bootloader/bootloader.bin.gz /github/workspace/bootloader.bin.gz

gzip -9 -k /app/micropython/ports/esp32/build-$1/partition_table/partition-table.bin
cp /app/micropython/ports/esp32/build-$1/partition_table/partition-table.bin /github/workspace/partition-table.bin
cp /app/micropython/ports/esp32/build-$1/partition_table/partition-table.bin.gz /github/workspace/partition-table.bin.gz

gzip -9 -k /app/micropython/ports/esp32/build-$1/ota_data_initial.bin
cp /app/micropython/ports/esp32/build-$1/ota_data_initial.bin /github/workspace/ota_data_initial.bin
cp /app/micropython/ports/esp32/build-$1/ota_data_initial.bin.gz /github/workspace/ota_data_initial.bin.gz

gzip -9 -k /app/micropython/ports/esp32/build-$1/micropython.bin
cp /app/micropython/ports/esp32/build-$1/micropython.bin /github/workspace/micropython.bin
cp /app/micropython/ports/esp32/build-$1/micropython.bin.gz /github/workspace/micropython.bin.gz

pip install littlefs-python
python /github/workspace/build/makefs.py --dir /github/workspace/build/python --out /github/workspace/fs.bin --block_count $2
gzip -9 -k /github/workspace/fs.bin
