import network
import prequests
import os
from machine import Pin
from esp32 import Partition
from creds import BASEURL, USERNAME, PASSWORD

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(USERNAME, PASSWORD)
        while not wlan.isconnected():
            pass
    return wlan


def do_disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)


def sync_blocks(url, partition):
    request = prequests.get(url)
    file_stream = zlib.DecompIO(request.raw)
    block = 0
    block_data = b""
    data_downloaded = file_stream.read(4096)
    while len(data_downloaded) != 0:
        partition.readblocks(block_num, block_data)
        if data_downloaded != block_data:
            partition.writeblocks(block_num, block_data)
        block += 1
        data_downloaded = file_stream.read(4096)
    r.close()
    print("Done DL of", 4096*block + len(data_downloaded))


def check_sync(name, partition):
    url = BASEURL + name + ".bin.gz"
    request = prequests.head(url, parse_headers=True)
    latest_version = request.headers['ETag']
    if open("current_version_"+name+".txt", "r").read() != latest_version:
        sync_blocks(url, partition)
        open("current_version_"+name+".txt", "w").write(latest_version)


if __name__ == "__main__":
    pin = Pin(2, Pin.OUT)
    pin.on()
    print('Connecting to network...')
    wlan = do_connect()
    print('Connected, network config:', wlan.ifconfig())
    pin.off()
    print('Syncing partition')
    partition = Partition.find(type=Partition.TYPE_DATA)[-1]
    check_sync("fs", partition)
    print('Sync done, mounting')
    os.mount(partition, '/')
    print('All complete')
