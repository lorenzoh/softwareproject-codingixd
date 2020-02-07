import json
from collections import defaultdict
from typing import Dict, Optional, List, Tuple
from argparse import ArgumentParser
from time import time

import cv2

from detector import Detector
from draw import draw_debug
from ledclient import LEDClient
from geomutils import contains

H, W = 439, 639

MARKERTIMEOUT = 3

REGIONS = {
    "platform": {
        "name": "platform",
        "rect": [H // 2, 0, H, W],
        "leds": [],
    },
    "cart3": {
        "name": "cart3",
        "rect": [0, 0, H // 2, W // 2],
        "leds": [
            ("bot5", "mid5", "top5"),
            ("bot6", "mid6", "top6"),
            ],
    },
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

def findregion(p: Tuple[int, int], regions) -> Optional["Region"]:
    for region in regions.values():
        if contains(region["rect"], p):
            return region["name"]
    else:
        return None
        

def update_regions(markers, regions, markerregions, markertimeouts):

    # refresh timeouts for detected markers
    for marker in markers:
        markertimeouts[marker["id"]] = time()

    # remove timed out markers from tracking
    t = time()
    for (marker_id, timeout) in markertimeouts.items():
        if timeout and t - timeout > MARKERTIMEOUT:
            markerregions[marker_id] = None

    # refresh/add regions for detected markers
    for marker in markers:
        markerregions[marker["id"]] = findregion(
            marker["p"], regions)

    return markerregions, markertimeouts


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
    ledclient = LEDClient(args.controllerurl)
    detector = Detector(args.cameraid)

    markerregions: Dict[str, str] = defaultdict(lambda: None)
    markertimeouts = defaultdict(lambda: None)

    try:
        while True:
            print("---")
            frame, markers = detector.get_markers()
            print(len(markers))
            markerregions, markertimeouts = update_regions(
                markers, REGIONS, markerregions, markertimeouts
            )
            print(json.dumps(dict(markerregions), indent=2))
            
            # count markers for every region
            region_counts = {region: 0 for region in REGIONS}
            for markerid, regionname in markerregions.items():
                if regionname is None:
                    continue
                region_counts[regionname] += 1
            
            for regionname, count in region_counts.items():
                light_region(regionname, count, ledclient)

            draw_debug(frame, markers, REGIONS)
            lh, lw = int(frame.shape[0]*2), int(frame.shape[1]*2)
            frame = cv2.resize(frame, (lw, lh))
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        detector.cleanup()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("controllerurl")
    parser.add_argument("cameraid", type=int)

    args = parser.parse_args()

    main(args)
