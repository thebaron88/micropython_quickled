from machine import Pin
import machine
import network
import socket


def do_download():
    s = socket.socket()
    s.connect(socket.getaddrinfo("BARON-DESKTOP.lan", 8093)[0][-1])
    bytes_in = b""
    while True:
        data = s.recv(1024)
        if data == b"":
            break
        bytes_in += data
    return bytes_in


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('BaronHomeWifi_N', 'BaronHomeWifi25')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def do_disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)


if __name__ == "__main__":
    pin = Pin(2, Pin.OUT)
    pin.on()
    do_connect()
    ota_bytes = do_download()
    exec(ota_bytes)
    pin.off()
