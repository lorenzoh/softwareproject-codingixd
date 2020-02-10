
from flask import Flask, jsonify, request
from gpiozero import RGBLED

from ledcontroller import LEDController

LEDS = {
    "rgb1": (2, 3, 4),
    "rgb2": (22, 27, 17),
    "rgb3": (11, 10, 9),
    "rgb4": (6, 0, 5),
    "a1": 13,
    "a2": 19,
    "a3": 26,
    "a4": 14,
}

app = Flask(__name__)

@app.route('/')
def smoketest():
    return ""

@app.route("/leds/")
def leds():
    return jsonify(list(controller.leds))

@app.route("/leds/<name>/on")
def led_on(name):
    controller.set_on(name)
    return ""

@app.route("/leds/<name>/off")
def led_off(name):
    controller.set_off(name)
    return ""

@app.route("/leds/<name>/color")
def led_color(name):
    r = 1 - float(request.args.get("r"))
    g = 1 - float(request.args.get("g"))
    b = 1 - float(request.args.get("b"))
    duration = float(request.args.get("duration", 0.))
    controller.leds[name].color = (r, g, b)
    if name not in controller.leds:
        return f"LED {name} not found", 404

        controller.set_color(name, (r, g, b), duration=duration)

    return " ".join([str(r), str(g), str(b)])



if __name__ == "__main__":
    controller = LEDController(LEDS)
    try:
        app.run()#debug=True)
    finally:
        controller.cleanup()
