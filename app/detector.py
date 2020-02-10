from typing import Tuple, Optional
from collections import defaultdict
import cv2
from time import time


from geomutils import centroid, contains

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
MARKERTIMEOUT = 3


class Detector:
    def __init__(
        self, regions, cameraid: int, aruco_dict=ARUCO_DICT, markertimeout=MARKERTIMEOUT
    ):
        self.regions = regions
        self.cameraid = cameraid
        self.aruco_dict = aruco_dict
        self.frame = None
        self.markers = []
        self.markerregions: Dict[str, str] = defaultdict(lambda: None)
        self.markertimeouts = defaultdict(lambda: None)
        self.markertimeout = markertimeout

    def setup(self):
        self.cam = cv2.VideoCapture(self.cameraid)

    def cleanup(self):
        self.cam.release()

    def process_frame(self):
        ret = False
        while not ret:
            ret, self.frame = self.cam.read()
        markers = get_markers(self.frame, self.aruco_dict)
        self.update_regions(markers)

        return {
            "markers": markers,
            "regions": self.markerregions
        }

    def update_regions(self, markers):

        # refresh timeouts for detected markers
        for marker in markers:
            self.markertimeouts[marker["id"]] = time()

        # remove timed out markers from tracking
        t = time()
        for (marker_id, timeout) in self.markertimeouts.items():
            if timeout and t - timeout > self.markertimeout:
                self.markerregions[marker_id] = None

        # refresh/add regions for detected markers
        for marker in markers:
            self.markerregions[marker["id"]] = findregion(marker["p"], self.regions)


def get_markers(frame, aruco_dict):
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict)
    if len(corners) > 0:
        return [
            {
                "id": int(id_),
                "p": centroid(list(corner.flatten())),
                "corners": list(corner.flatten()),
            }
            for (id_, corner) in zip(ids, corners)
        ]
    else:
        return []


def findregion(p: Tuple[int, int], regions) -> Optional["Region"]:
    for region in regions.values():
        if contains(region["rect"], p):
            return region["name"]
    else:
        return None
