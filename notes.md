# WSL Instructions
## Guide
### Environment Setup
apt-get install build-essential libreadline-dev libffi-dev git pkg-config gcc-arm-none-eabi libnewlib-arm-none-eabi python2 python3 python3-venv

export MICROPY=/mnt/c/Users/Mark/esp/micropython
mkdir -p $MICROPY
export ESPIDF=/mnt/c/Users/Mark/esp/esp-idf
mkdir -p $ESPIDF

### Download Repos
git clone --recurse-submodules https://github.com/micropython/micropython.git $MICROPY
git clone https://github.com/espressif/esp-idf.git $ESPIDF

### Checkout accepted version
cd $MICROPY/ports/esp32
make ESPIDF=

cd $ESPIDF
git checkout 4c81978a3e2220674a432a588292a4c860eef27b
git submodule update --init --recursive

### Make Python environment
cd /mnt/c/Users/Mark/esp/
python3 -m venv build-venv
source build-venv/bin/activate
pip install --upgrade pip
pip install -r $ESPIDF/requirements.txt
pip install virtualenv

### Download esp tools
./install.sh
source $ESPIDF/export.sh

### Build MicroPython tools
cd $MICROPY/mpy-cross/
make mpy-cross

### Build MicroPython port
cd $MICROPY/ports/esp32/
vim GNUmakefile ????????????
make submodules
make

### Enable environment
source /mnt/c/Users/Mark/esp/build-venv/bin/activate
source /mnt/c/Users/Mark/esp/esp-idf/export.sh

### Build custom version
make USER_C_MODULES=../../../micropythonmodules CFLAGS_EXTRA="-DMODULE_QUICKLED_ENABLED=1" all -j24

### Flash version
SET PATH=C:\Users\Mark\AppData\Local\Programs\Python\Python39;C:\Users\Mark\AppData\Local\Programs\Python\Python39\Scripts;%PATH%
esptool.py.exe --before no_reset erase_flash
esptool.py.exe --chip esp32 --port COM3 -b 921600 write_flash -z 0x1000 firmware.bin