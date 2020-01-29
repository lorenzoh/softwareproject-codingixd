import json
from collections import defaultdict
from typing import Dict, Optional, Tuple
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
        "leds": {
            "rgb": []
        }
    },
    "cart1": {
        "name": "cart1",
        "rect": [0, 0, H // 2, W // 2],
        "leds": {
            "rgb": ["rgb1", "rgb2"]
        }
    },
    "cart2": {
        "name": "cart2",
        "rect": [0, W // 2, H // 2, W],
        "leds": {
            "rgb": ["rgb3", "rgb4"]
        }
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

            # turn on led if 
            for regionname, count in region_counts.items():
                leds = REGIONS[regionname]["leds"]["rgb"]
                if count == 0:
                    for led in leds:
                        ledclient.set_color(led, (0, .4, 0))
                elif 1 <= count <= 2:
                    print(count)
                    for led in leds:
                        ledclient.set_color(led, (.5, .5, 0))
                else:
                    for led in leds:
                        ledclient.set_color(led, (.5, 0, 0))

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
