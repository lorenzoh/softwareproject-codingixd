import sys
from yeelight import discover_bulbs
from yeelight import Bulb, BulbException
from yeelight import TemperatureTransition,SleepTransition,SceneClass
from yeelight import Flow
import random
import time


TRANSITION_DURATION = 1
WAIT_DURATION = 5


ips = [f"192.168.137.{n}" for n in (sys.argv[1], sys.argv[2], sys.argv[3])]
bulbs = [Bulb(ip, effect="smooth", duration=TRANSITION_DURATION*1000) for ip in ips]

# Reset bulbs
for bulb in bulbs:
    bulb.turn_off(duration=0)
    bulb.set_rgb(red=255,green=255,blue=255)
    bulb.set_color_temp(5000, duration=0)
    bulb.set_brightness(1, duration=0)

time.sleep(1)

# main loop

while True:
    try:
        for i in range(1, 4):
            bulbsubset = bulbs[:i]
            for bulb in bulbsubset: bulb.set_brightness(1, duration=0)
            for bulb in bulbsubset: bulb.turn_on()
            for bulb in bulbsubset: bulb.set_brightness(100)
            time.sleep(TRANSITION_DURATION + WAIT_DURATION)

            for bulb in bulbsubset[::-1]:
                bulb.set_brightness(1)
                bulb.turn_off()
                time.sleep(.2)
            time.sleep(TRANSITION_DURATION + .5)
    except BulbException as b:
        print("ERROR: ", str(b))
        continue
    except Exception as e:
        for bulb in bulbs:
            bulb.turn_off()
        raise e

