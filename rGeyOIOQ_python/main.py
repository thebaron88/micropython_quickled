import machine
import json
machine.freq(240000000)
print("Hello There")

from mqtt import MQTTClient
from machine import Pin
import onewire
import time, ds18x20

output_pin = Pin(13, Pin.OPEN_DRAIN, None, value=0)
output_pin.value(0)

def sub_cb(topic, msg, setpoints):
    data = json.loads(msg)
    setpoints["min"] = data["min"]
    setpoints["max"] = data["max"]

def main(client_id="loopsensor", server="baron-linux-desktop"):
    one_wire = onewire.OneWire(Pin(15)) # create a OneWire bus on GPIO12
    dallas_temps = ds18x20.DS18X20(one_wire)
    temp_sensors = dallas_temps.scan()
    last_temps = [0 for device_handle in temp_sensors]
    setpoints = {'min': 40, 'max': 60}
    c = MQTTClient(client_id, server, keepalive=10)
    c.set_callback(lambda topic, msg: sub_cb(topic, msg, setpoints))
    c.connect()
    c.subscribe(b"heating/calls/boiler")
    while True:
        dallas_temps.convert_temp()
        time.sleep(1)
        temps = [dallas_temps.read_temp(device_handle) for device_handle in temp_sensors]
        one = False
        for i in range(len(temps)):
            if temps[i] != last_temps[i]:
                one = True
                c.publish(b"heating/loop/temp"+str(i), str(temps[i]))
        if not one:
            c.ping()

        if max(temps) > setpoints["max"]:
            output_pin.value(0)
        elif min(temps) < setpoints["min"]:
            output_pin.value(1)

        last_temps = temps
        for i in range(4):
            c.check_msg()
            time.sleep(1)

if __name__ == "__main__":
    while True:
        try:
            connect_to_network("loopsensor")
            main()
        except:
            pass
