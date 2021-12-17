# micropython_quickled
Micropython module which allows python to pump data into the ws2811 leds at full speed.

idf.py -D MICROPY_BOARD=GENERIC_OTA_LED -B build-GENERIC_OTA_LED -DUSER_C_MODULES=/home/baron/micropython_quickled/quickled/micropython.cmake all
