from machine import Pin
from neopixel import NeoPixel
import utime
import machine
import esp
import esp32
import quickled

THIS_LEDS = const(60)
MAX_LEDS = const(500)
LOOPS = const(10)

@micropython.native
def hsl_to_rgb(h, s, l):
    c = (1 - abs((2 * l) - 1)) * s
    hh = h / 60
    x = c * (1 - abs((hh % 2) - 1))
    c = int(c * 255)
    x = int(x * 255)
    if hh <= 1:
        return c, x, 0
    if hh <= 2:
        return x, c, 0
    if hh <= 3:
        return 0, c, x
    if hh <= 4:
        return 0, x, c
    if hh <= 5:
        return x, 0, c
    if hh <= 7:
        return c, 0, x

@micropython.native
def hsv2rgb_raw(hue: int, saturation: int, value: int) -> int:
    invsat = 255 - saturation
    brightness_floor = (value * invsat) // 256
    color_amplitude = value - brightness_floor
    section = hue // 64
    offset = hue % 64

    rampup = offset
    rampdown = 64 - offset

    rampup_amp_adj = (rampup * color_amplitude) // 64
    rampdown_amp_adj = (rampdown * color_amplitude) // 64

    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    if section < 1:
        return rampdown_adj_with_floor, rampup_adj_with_floor, brightness_floor
    if section < 2:
        return brightness_floor, rampdown_adj_with_floor, rampup_adj_with_floor
    return rampup_adj_with_floor, brightness_floor, rampdown_adj_with_floor

@micropython.native
def hsv2rgb_raw_fast(hue: int, saturation: int, value: int, pixels) -> int:
    invsat = 255 - saturation
    brightness_floor = (value * invsat) // 256
    color_amplitude = value - brightness_floor
    section = hue // 64
    offset = hue % 64

    rampup = offset
    rampdown = 64 - offset

    rampup_amp_adj = (rampup * color_amplitude) // 64
    rampdown_amp_adj = (rampdown * color_amplitude) // 64

    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    if section < 1:
        pixels[0] = rampdown_adj_with_floor
        pixels[1] = rampup_adj_with_floor
        pixels[2] = brightness_floor
    if section < 2:
        pixels[0] = brightness_floor
        pixels[1] = rampdown_adj_with_floor
        pixels[2] = rampup_adj_with_floor
    pixels[0] = rampup_adj_with_floor
    pixels[1] = brightness_floor
    pixels[2] = rampdown_adj_with_floor

T0H, T0L = 250, 1000
T1H, T1L = 1000, 250
RET = 500

T0H, T0L = T0H//50, T0L//50
T1H, T1L = T1H//50, T1L//50
RET = RET//50

#pulses_list = bytearray([0] * (8 * 2) * MAX_LEDS * 3)


@micropython.native
def send_data(memory_view):
    pulses = memoryview(pulses_list)
    pack_data(memory_view, pulses)
    r.write_pulses(tuple(pulses), start=1)
    #r.wait_done(timeout=3008000)


@micropython.native
def pack_data(memory_view, pulses):
    pos = 0
    for byte in memory_view:
        for bit in range(8):
            if byte & (2 ** (8 - bit)) == 0:
                pulses[pos] = T0H
                pos += 1
                pulses[pos] = T0L
                pos += 1
            else:
                pulses[pos] = T1H
                pos += 1
                pulses[pos] = T1L
                pos += 1
    pulses[-1] = RET

@micropython.native
def do_led_fast(pixel_pin, num):
    pixel_view = memoryview(pixel_buff)
    #for i in range(MAX_LEDS):
    #    hsv2rgb_raw_fast(0, 255, 1, pixel_view[i * 3: i * 3 + 3])
    hsv2rgb_raw_fast(num*4, 255, 10, pixel_view[num * 3: num * 3 + 3])
    #esp.neopixel_write(pixel_pin, pixel_off, True)
    #send_data(pixel_off)
    cexample.neopixel_fast_write(pixel_pin, pixel_buff)
    #for o in range(10000):
    #    for p in range(10):
    #        pass

@micropython.native
def do_led(pixel_pin, num):
    pixel_buff = bytearray(3 * MAX_LEDS)
    #pixel_off[num * 3: num * 3 + 3] = bytearray(hsl_to_rgb(num*4, 1, 0.5))
    #pixel_buff = bytearray(3 * MAX_LEDS)
    pixel_off = memoryview(pixel_buff)
    #for i in range(MAX_LEDS):
    #    pixel_buff[i * 3: i * 3 + 3] = bytearray(hsv2rgb_raw(0, 255, 1))
    pixel_buff[num * 3: num * 3 + 3] = bytearray(hsv2rgb_raw(num*4, 255, 255))
    #esp.neopixel_write(pixel_pin, pixel_off, True)
    #send_data(pixel_off)
    quickled.write(pixel_pin, pixel_buff)
    #for o in range(10000):
    #    for p in range(10):
    #        pass


def do_animation(pixel_pin):
    for l in range(LOOPS):
        t = utime.ticks_us()
        for i in range(THIS_LEDS):
            do_led(pixel_pin, i)
        for i in range(THIS_LEDS):
            do_led(pixel_pin, THIS_LEDS - i - 1)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format("Fill", delta / 1000))


if __name__ == "__main__":
    machine.freq(240000000)
    pin = Pin(2, Pin.OUT)
    pin.on()

    pixel_pin = Pin(13, Pin.OUT)
    #r = esp32.RMT(0, pin=pixel_pin, clock_div=4)
    do_animation(pixel_pin)

    #
    #cexample.neopixel_fast_write(pixel_pin, bytearray([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0]))