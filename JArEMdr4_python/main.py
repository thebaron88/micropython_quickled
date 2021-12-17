import quickled
import machine
import random
import time

def res():
    machine.reset()

MAX_BRIGHT = 255 // 3
MAX_LEDS = 4 * 50

def do_demo(pixel_pin):
    i = 1
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([MAX_BRIGHT]*MAX_LEDS)
    while True:
        hue = bytearray([x % 256 for x in list(range(0+i, MAX_LEDS+i))])
        quickled.write_hsv(pixel_pin, hue, sat, val)
        i += 1

STEP = 8
def do_christmas_skip(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([0]*MAX_LEDS)
    color = 0
    skip = 2
    while True:
        skip = ((skip - 2 + random.randint(1, 3)) % 4 + 2)
        hit = random.randint(0, skip-1)
        color = (color + random.randint(30, 255-30)) % 256
        for i in range(0, MAX_LEDS):
            if i % skip == hit:
                while val[i] > 0 + STEP:
                    quickled.write_hsv(pixel_pin, hue, sat, val)
                    val[i] -= STEP
                val[i] = 0

                hue[i] = color

                while val[i] < MAX_BRIGHT - STEP:
                    quickled.write_hsv(pixel_pin, hue, sat, val)
                    val[i] += STEP
                val[i] = MAX_BRIGHT

                quickled.write_hsv(pixel_pin, hue, sat, val)

        skip = ((skip - 2 + random.randint(1, 3)) % 4 + 2)
        hit = random.randint(0, skip-1)
        color = (color + random.randint(30, 255-30)) % 256
        for i in range(MAX_LEDS-1, -1, -1):
            if i % skip == hit:
                while val[i] > 0 + STEP:
                    quickled.write_hsv(pixel_pin, hue, sat, val)
                    val[i] -= STEP
                val[i] = 0

                hue[i] = color

                while val[i] < MAX_BRIGHT - STEP:
                    quickled.write_hsv(pixel_pin, hue, sat, val)
                    val[i] += STEP
                val[i] = MAX_BRIGHT
                
                quickled.write_hsv(pixel_pin, hue, sat, val)


def sub_cb(topic, msg, pixel_pin):
    r, g, b = msg[1:3], msg[3:5], msg[5:7]
    #sat = bytearray([160]*MAX_LEDS)
    #val = bytearray([255//2]*MAX_LEDS)
    #hue = bytearray([(x//8) % 256 for x in list(range(0+400, MAX_LEDS+400))])
    buff = bytearray([int(r, 16),int(g, 16),int(b, 16)]*MAX_LEDS)
    quickled.write(pixel_pin, buff)


def do_white_test(pixel_pin):
    from mqtt import MQTTClient
    c = MQTTClient("chrimbo_tree", "baron-linux-desktop", keepalive=10)
    c.set_callback(lambda topic, msg: sub_cb(topic, msg, pixel_pin))
    c.connect()
    c.subscribe(b"color/set")
    while True:
        for i in range(10):
            c.check_msg()
            time.sleep(1)
        c.ping()


def main():
    pixel_pin = machine.Pin(13, machine.Pin.OUT)
    #do_white_test(pixel_pin)
    do_christmas_skip(pixel_pin)

machine.freq(240000000)
print("I am", machine.unique_id())
#do_disconnect()
#print(ota_bytes)
connect_to_network("christmas_tree")
main()
