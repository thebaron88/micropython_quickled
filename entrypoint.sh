#!/usr/bin/env bash
set -e

. $IDF_PATH/export.sh

cd /app/micropython/ports/esp32
make BOARD=GENERIC_OTA USER_C_MODULES=/github/workspace/quickled/micropython.cmake
