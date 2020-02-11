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
from flask_cors import CORS

H, W = 439, 639
TRANSITION_TIMEOUT = 5
CAPACITY = 8
DATA = {}
P = ".state"
DASHBOARD_OUT = {"regions": {}, "lastNSeconds": TRANSITION_TIMEOUT}

CART_START = 200
CART_HEIGHT = 50

REGIONS = {
    "platform": {
        "name": "platform",
        "rect": [0, 0, CART_START, W],
        "ledgroups": [],
    },
    "cart1": {
        "name": "cart1",
        "rect": [CART_START, 0, CART_START + CART_HEIGHT, W // 3],
        "ledgroups": [5, 6],
    },
    "cart2": {
        "name": "cart2",
        "rect": [CART_START, W//3, CART_START + CART_HEIGHT, 2 * (W//3)],
        "ledgroups": [3, 4],
    },
    "cart3": {
        "name": "cart3",
        "rect": [CART_START, 2*(W//3), CART_START + CART_HEIGHT, W],
        "ledgroups": [1, 2],
    },
}


GROUPSTATE = defaultdict(lambda: None)

def set_leds(ledgroups, n, ledclient):
    for ledgroup in ledgroups:
        currentn = GROUPSTATE[ledgroup]
        if currentn != n:
            ledclient.set_group(ledgroup, n)
            GROUPSTATE[ledgroup] = n
            

def light_region(regionname: str, count: int, ledclient: LEDClient):
    leds: List[Tuple[str, str, str]] = REGIONS[regionname]["ledgroups"]
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

                DASHBOARD_OUT["regions"][regionname] = {
                    "id": regionname,
                    "n": n,
                    "max": CAPACITY,
                    "entered": len(intransitions[regionname]),
                    "exited": len(outtransitions[regionname]),
                }

            regions_prev = regions.copy()
            with open(P, "w") as o:
                json.dump(DASHBOARD_OUT, o)

            draw_debug(detector.frame, detections["markers"], detector.regions)
            lh, lw = int(detector.frame.shape[0]*2), int(detector.frame.shape[1]*2)
            frame = cv2.resize(detector.frame, (lw, lh))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        detector.cleanup()

app = Flask(__name__)
CORS(app)

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