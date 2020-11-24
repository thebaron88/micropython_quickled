import quickled
import random
import utime
import machine

MAX_LEDS = 5*50


def timeit(method):
    def timed(*args, **kw):
        t = utime.ticks_us()
        result = method(*args, **kw)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms for 1 loop'.format(method.__name__, delta / 1000))
        t = utime.ticks_us()
        return result
    return timed


def shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]


def do_christmas_rand(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([255]*MAX_LEDS)
    pix_list = list(range(0, MAX_LEDS))
    col_list = [x % 256 for x in list(range(0, MAX_LEDS))]
    while True:
        shuffle(pix_list)
        shuffle(col_list)
        for i in pix_list:
            hue[i] = col_list[i]
            quickled.write_hsv(pixel_pin, hue, sat, val)


def do_christmas_skip(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([255]*MAX_LEDS)
    while True:
        skip = random.randint(2, 5)
        color = random.randint(0, 255)
        for i in range(0, MAX_LEDS):
            if i % skip == 0:
                hue[i] = color
            quickled.write_hsv(pixel_pin, hue, sat, val)
        skip = random.randint(2, 5)
        color = random.randint(0, 255)
        for i in range(MAX_LEDS-1, -1, -1):
            if i % skip == 0:
                hue[i] = color
            quickled.write_hsv(pixel_pin, hue, sat, val)


def do_christmas_hue(pixel_pin):
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([32]*MAX_LEDS)
    num = 0
    while True:
        quickled.write_hsv(pixel_pin, bytearray([x % 256 for x in range(num, num+(MAX_LEDS*1), 1)]), sat, val)
        num += 1


def main():
    pixel_pin = machine.Pin(13, Pin.OUT)
    do_christmas_rand(pixel_pin)

machine.freq(240000000)
#do_disconnect()
print(ota_bytes)
main()
