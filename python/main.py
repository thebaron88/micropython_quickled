import quickled
import random
import utime
import machine
import time

if machine.unique_id() == b'Nope':
    MAX_LEDS = 5 * 50  # 60
    USED_LEDS = 2 * 50  # 60
    MAX_BRIGHT = 255
    FADE_LIMIT = 0
else:
    MAX_LEDS = 5 * 50
    USED_LEDS = 5 * 50  # 60
    MAX_BRIGHT = 255  # 104W at 255, 31W at 32
    FADE_LIMIT = 0

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
    val = bytearray([MAX_BRIGHT]*MAX_LEDS)
    pix_list = list(range(0, MAX_LEDS))
    col_list = [x % 256 for x in list(range(0, max(MAX_LEDS, 255)))]
    start = time.time()
    while True:
        shuffle(pix_list)
        shuffle(col_list)
        for i in pix_list:
            hue[i] = col_list[i]
            quickled.write_hsv(pixel_pin, hue, sat, val)
        #fade = min((time.time() - start) // (7200 // 255), 255)
        #val = bytearray([MAX_BRIGHT - fade] * MAX_LEDS)


def do_christmas_rand_few(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([0]*MAX_LEDS)
    pix_list = []
    col_list = [x % 256 for x in list(range(0, max(MAX_LEDS, 255)))]
    sat_list = list([255 if i > 50 else 0 for i in range(400)])
    on = False
    while True:
        if len(pix_list) == 0:
            pix_list = list(range(0, MAX_LEDS))
            shuffle(pix_list)
            shuffle(col_list)
            shuffle(sat_list)
        i = pix_list.pop()
        hue[i] = col_list[i]
        val[i] = MAX_BRIGHT
        sat[i] = sat_list[i]
        quickled.write_hsv(pixel_pin, hue, sat, val)
        for _ in range(5):
            for i in range(len(val)):
                if val[i] > 24:
                    val[i] -= 2
            quickled.write_hsv(pixel_pin, hue, sat, val)


def do_christmas_rand_good(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([0]*MAX_LEDS)
    pix_list = list(range(0, MAX_LEDS))
    col_list = list(range(256)) * ((USED_LEDS // 255) + 1)
    sat_list = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0] * ((USED_LEDS // 12) + 1)
    shuffle(pix_list)
    shuffle(col_list)
    shuffle(sat_list)
    todo = USED_LEDS
    while True:
        if todo > 0:
            todo -= 1
            i = pix_list.pop()
            hue[i] = col_list.pop()
            val[i] = MAX_BRIGHT
            sat[i] = sat_list.pop()
        quickled.write_hsv(pixel_pin, hue, sat, val)
        for i in range(len(val)):
            if val[i] > FADE_LIMIT:
                val[i] -= 1
                if val[i] <= FADE_LIMIT:
                    todo += 1
                    pix_list.append(i)
                    col_list.append(hue[i])
                    sat_list.append(sat[i])
                    shuffle(pix_list)
                    shuffle(col_list)
                    shuffle(sat_list)


FADE = False
SPEED = 8  # * 8
def do_christmas_rand_fade(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([0]*MAX_LEDS)
    fade = list(range(0, MAX_BRIGHT+1, SPEED))
    pix_list = list(range(0, MAX_LEDS))
    col_list = [x % 256 for x in list(range(0, MAX_LEDS))]
    while True:
        shuffle(pix_list)
        shuffle(col_list)
        for i in pix_list:
            if FADE:
                if val[i] != 0:
                    for value in reversed(fade):
                        val[i] = value
                        quickled.write_hsv(pixel_pin, hue, sat, val)
            else:
                val[i] = MAXBRIGHT
            hue[i] = col_list[i]
            if FADE:
                for value in fade:
                    val[i] = value
                    quickled.write_hsv(pixel_pin, hue, sat, val)
            quickled.write_hsv(pixel_pin, hue, sat, val)


def do_christmas_skip(pixel_pin):
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([MAX_BRIGHT]*MAX_LEDS)
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
    val = bytearray([MAX_BRIGHT]*MAX_LEDS)
    num = 0
    while True:
        quickled.write_hsv(pixel_pin, bytearray([x % 256 for x in range(num, num+(MAX_LEDS*1), 1)]), sat, val)
        num -= 1


def main():
    pixel_pin = machine.Pin(13, Pin.OUT)
    do_christmas_rand_good(pixel_pin)

machine.freq(240000000)
print("I am", machine.unique_id())
#do_disconnect()
#print(ota_bytes)
main()
