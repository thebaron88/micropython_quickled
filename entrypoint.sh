#!/bin/sh

# `$*` expands the `args` supplied in an `array` individually
# or splits `args` in a string separated by whitespace.
sh -c "echo $*"
make BOARD=GENERIC_OTA USER_C_MODULES=/usercmodule/quickled/quickled/quickled/micropython.cmake

