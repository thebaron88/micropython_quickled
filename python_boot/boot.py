import network
import prequests
import os
import zlib
import time
import sys
from machine import Pin
from esp32 import Partition
from creds import BASEURL, USERNAME, PASSWORD

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(USERNAME, PASSWORD)
        time_passed = 0
        while not wlan.isconnected():
            time.sleep(1)
            time_passed += 1
            if time_passed > 20:
                return None
    return wlan


def do_disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)


gzdict_sz = 16 + 15
def sync_blocks(url, partition):
    request = prequests.get(url)
    file_stream = zlib.DecompIO(request.raw, gzdict_sz)
    block_num = 0
    block_data = bytearray(4096)
    dl_buffer = bytearray(4096)
    data_downloaded = file_stream.readinto(dl_buffer)
    while data_downloaded != 0:
        print(block_num)
        partition.readblocks(block_num, block_data)
        if dl_buffer != block_data:
            print("Writing")
            partition.writeblocks(block_num, dl_buffer)
        block_num += 1
        data_downloaded = file_stream.readinto(dl_buffer)
    request.close()
    print("Done DL of", 4096*block_num + data_downloaded)


def check_sync(name, partition):
    url = BASEURL + name + ".bin.gz"
    request = prequests.head(url, parse_headers=True)
    latest_version = request.headers['ETag']
    file_name = "current_version_"+name+".txt"
    if file_name not in os.listdir("/") or open(file_name, "r").read() != latest_version:
        print("Updating to version", latest_version)
        sync_blocks(url, partition)
        open(file_name, "w").write(latest_version)
        return True
    else:
        print("Already at version", latest_version)
        return False

def connect_to_network():
    print('Connecting to network...')
    try:
        wlan = do_connect()
        print('Connected, network config:', wlan.ifconfig())
        return True
    except:
        pass
    print("Failed to connect to the network.")
    return False


def find_partition(label):
    python_boot_partitons = Partition.find(type=Partition.TYPE_DATA, label="vfs")
    if len(python_boot_partitons) == 1:
        print("Partition", label, "found")
        return python_boot_partitons[0]
    print("Could not find partition", label)
    sys.exit()

if __name__ == "__main__":
    pin = Pin(2, Pin.OUT)
    pin.on()

    connected = connect_to_network()
    python_boot_partiton = find_partition("vfs")
    python_app_partiton = find_partition("vfs_1")

    if connected:
        current_mpy_partition = Partition(Partition.RUNNING)
        current_mpy_partition.mark_app_valid_cancel_rollback()  # A MPy update is only successful if the WIFI works

        print('Syncing python boot partition')  # Very rare and dangerous.
        if check_sync("python_boot", python_boot_partiton):
            machine.soft_reset()  # It is only this partition that changed, not the FW

        print('Syncing python app partition')  # Pretty common
        if check_sync("python", python_app_partiton):
            pass  # We mount afterwards, so its not currently in use anyway

        if check_sync("app", ota_partition):
            ota_partition.set_boot()
            machine.reset()  # This was a full fat FW update, reboot.

        do_disconnect()
    
    print('Mounting')
    os.mount(python_app_partiton, '/')
    pin.off()
