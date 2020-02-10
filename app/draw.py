import cv2
import numpy as np


def draw_marker(img, marker):
    corner, id_ = marker["corners"], marker["id"]
    x1, y1, x2, y2, x3, y3, x4, y4 = corner
    cv2.polylines(img, [np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.int32)], True, (255, 0, 0), 2)
    centroid = int(np.mean([x1, x2, x3, x4]) + 10), int(np.mean([y1, y2, y3, y4]) - 10)
    cv2.putText(img, str(id_), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


def draw_region(image, region):
    y1, x1, y2, x2 = region["rect"]
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0))
    cv2.putText(image, f"{region['name']}", (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 0, 0), 2)


def draw_debug(frame, markers, regions):
    for marker in markers:
        draw_marker(frame, marker)
    for region in regions.values():
        draw_region(frame, region)
    return frame