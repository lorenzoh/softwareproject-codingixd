import requests
import json


class LEDClient:

    def __init__(self, url):
        self.url = url
        r = requests.get(url)
        r.raise_for_status()

    def get_leds(self):
        r = requests.get(f"{self.url}/leds", timeout=3)
        r.raise_for_status()
        return r.json()

    def set_color(self, name, color, duration=0):
        r, g, b = color
        r = requests.get(
            f"{self.url}/leds/{name}/color",
            params={
                "r": r,
                "g": g,
                "b": b,
                "duration": duration
            },
            timeout=3)
        r.raise_for_status()

    def set_on(self, name):
        r = requests.get(f"{self.url}/leds/{name}/on", timeout=3)
        r.raise_for_status()

    def set_off(self, name):
        r = requests.get(f"{self.url}/leds/{name}/off", timeout=3)
        r.raise_for_status()

