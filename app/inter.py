from app import *

detector = Detector(0)
markerregions: Dict[str, str] = defaultdict(lambda: None)
markertimeouts = defaultdict(lambda: None)

markers = []
while not markers:
    markers = detector.get_markers()