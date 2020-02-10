from typing import Dict
from gpiozero import RGBLED, LED
from loguru import logger


class LEDController:

    def __init__(self, leds = {}):
        self.leds: Dict[Any, RGBLED] = {}
        print("HI")
        for (name, pins) in leds.items():
            self.add_led(name, pins)

    def add_led(self, name, pins):
        assert (not self.leds.get(name)), f"LED {name} already exists!"
        logger.info(f"Adding LED with pins {pins}")
        if isinstance(pins, int):
            self.leds[name] = LED(pins)
        else:
            self.leds[name] = RGBLED(*pins, initial_value=(.7, 1, 1))

    def set_on(self, name):
        led = self.leds[name] 
        assert isinstance(led, LED)
        print("ON")
        led.off()

    def set_off(self, name):
        led = self.leds[name] 
        if isinstance(led, LED):
            led.on()
        else:
            led.color = (1, 1, 1)

    def set_color(self, name, color, duration=0.):
        # TODO: implement slow transition with background thread
        print(leds[name])
        led = self.leds[name]
        if duration == 0:
            led.color = color
        elif duration > 0:
            self._transition_led(led, color, duration)
        
    def cleanup(self):
        for name, led in self.leds.items():
            logger.info(f"Closing LED {name}")
            led.close()

    def _transition_led(self, led, color, duration):
        # TODO: implement
        led.color = color