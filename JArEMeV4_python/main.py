import machine
import json
import time
import quickled
import ntptime

NAME = "test_leder"
machine.freq(240000000)
print("Hello There")

from mqtt import MQTTClient


def sub_cb(topic, msg):
    data = json.loads(msg)
    print(data)

MAX_LEDS = 4 * 50
def main(client_id=NAME, server="baron-linux-desktop"):
    ntptime.settime()
    pixel_pin = machine.Pin(13, machine.Pin.OUT)
    hue = bytearray([0]*MAX_LEDS)
    sat = bytearray([255]*MAX_LEDS)
    val = bytearray([0]*MAX_LEDS)
    #c = MQTTClient(client_id, server, keepalive=10)
    #c.set_callback(sub_cb)
    #c.connect()
    #c.subscribe(b"test/sub/"+NAME)
    i = 0
    h = 0
    while True:
        #c.publish(b"test/"+NAME, str(i))
        #c.ping()
        #c.check_msg()
        i += 1
        print(time.localtime(), "200 leds", 200*1000)
        for _ in range(1000):
            yr, mon, day, hr, min, sec, _, _ = time.localtime()
            # hue = bytearray([x % 256 for x in list(range(0+h, MAX_LEDS+h))])
            val = bytearray([0]*MAX_LEDS)
            hr_led = ((((hr * 60) + min) // 24) + 30) % 60
            min_led = (min + 30) % 60
            sec_led = (sec + 30) % 60
            val[hr_led] = 255//6
            hue[hr_led] = 85*0
            val[min_led] = 255//6
            hue[min_led] = 85*2
            val[sec_led] = 255//6
            hue[sec_led] = 85*1
            quickled.write_hsv(pixel_pin, hue, sat, val)
            h += 1

if __name__ == "__main__":
    connect_to_network(NAME)
    main()
