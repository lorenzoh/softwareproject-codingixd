from random import random
import json
import threading
from collections import defaultdict
from time import time, sleep
from typing import Dict, Optional, List, Tuple
from argparse import ArgumentParser

import cv2
from flask import Flask

from detector import Detector
from draw import draw_debug
from ledclient import LEDClient
from geomutils import contains

H, W = 439, 639
TRANSITION_TIMEOUT = 5
CAPACITY = 8
DATA = {}
P = ".state"
DASHBOARD_OUT = {"regions": {}}

REGIONS = {
    "platform": {
        "name": "platform",
        "rect": [H // 2, 0, H, W],
        "leds": [],
    },
    #"cart3": {
    #    "name": "cart3",
    #    "rect": [0, 0, H // 2, W // 2],
    #    "leds": [
    #        ("bot5", "mid5", "top5"),
    #        ("bot6", "mid6", "top6"),
    #        ],
    #},
    "cart2": {
        "name": "cart2",
        "rect": [0, 0, H // 2, W // 2],
        "leds": [
            ("bot3", "mid3", "top3"),
            ("bot4", "mid4", "top4"),
            ],
    },
    "cart1": {
        "name": "cart1",
        "rect": [0, W // 2, H // 2, W],
        "leds": [
            ("bot1", "mid1", "top1"),
            ("bot2", "mid2", "top2"),
            ],
    },
}


def set_leds(ledgroups, n_on, ledclient):
    ons = ([True] * n_on) + ([False] * (len(ledgroups[0])-n_on))
    for leds in ledgroups:
        for led, on in zip(leds, ons):
            if on:
                ledclient.set_on(led)
            else:
                ledclient.set_off(led)


def light_region(regionname: str, count: int, ledclient: LEDClient):
    leds: List[Tuple[str, str, str]] = REGIONS[regionname]["leds"]
    # region is not a cart
    if not leds:
        return
    # cart empty
    elif count == 0:
        set_leds(leds, 3, ledclient)
    # cart lightly filled
    elif count <= 3:
        set_leds(leds, 2, ledclient)
    # cart filled
    elif count <= 6:
        set_leds(leds, 1, ledclient)
    # cart full
    else:
        set_leds(leds, 0, ledclient)


def main(args):
    #ledclient = LEDClient(args.controllerurl)
    detector = Detector(REGIONS, args.cameraid)

    intransitions = defaultdict(list)
    outtransitions = defaultdict(list)

    detector.setup()
    regions_prev = None
    try:
        while True:
            detections = detector.process_frame()
            regions = detections["regions"]

            if regions_prev is not None:

                for marker_id in regions.keys():
                    region = regions[marker_id]
                    region_prev = regions_prev.get(marker_id, None)
                    if region != region_prev:
                        t = time()
                        intransitions[region].append(t)
                        outtransitions[region_prev].append(t)
            

            for ts in (intransitions, outtransitions):
                for (r, tstamps) in ts.items():
                    while tstamps and time() > (tstamps[0] + TRANSITION_TIMEOUT):
                        tstamps.pop()

            for regionname, region in REGIONS.items():
                n = len([... for rn in regions.values() if rn == regionname])
                #light_region(regionname, n, ledclient)

                print("setting")
                DASHBOARD_OUT["regions"][regionname] = {
                    "id": regionname,
                    "n": n,
                    "max": CAPACITY,
                    "entered": len(intransitions),
                    "exited": len(outtransitions),
                }

            regions_prev = regions.copy()
            with open(P, "w") as o:
                json.dump(DASHBOARD_OUT, o)
    finally:
        detector.cleanup()

app = Flask(__name__)

@app.route("/")
def index():
    with open(P, "r") as f:
        s = f.read()
    return json.dumps(s)



if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("controllerurl")
    parser.add_argument("cameraid", type=int)

    args = parser.parse_args()
    #main(args)
    t = threading.Thread(target=main, args=(args,), daemon=True)
    t.start()

    app.run(debug=True)