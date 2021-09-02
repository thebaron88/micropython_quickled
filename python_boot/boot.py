import network
import prequests
import os
import zlib
import time
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
    else:
        print("Already at version", latest_version)


if __name__ == "__main__":
    pin = Pin(2, Pin.OUT)
    pin.on()
    partition = Partition.find(type=Partition.TYPE_DATA, label="vfs_1")[0]
    if False:
        print('Connecting to network...')
        try:
            wlan = do_connect()
            print('Connected, network config:', wlan.ifconfig())
            print('Syncing partition')
            try:
                check_sync("DYNAMIC", partition)
            except:
                print("Fail to check sync, skipping.")
        except:
            print("Failed to connect to the network, skipping.")
    pin.off()
    print('Mounting')
    os.mount(partition, '/')
    print('All complete')
