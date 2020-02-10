import numpy as np

def centroid(corners):
    x1, y1, x2, y2, x3, y3, x4, y4 = corners
    return np.mean([y1, y2, y3, y4]), np.mean([x1, x2, x3, x4])

def contains(rect, p):
    ry1, rx1, ry2, rx2 = rect
    y, x = p
    return (ry1 <= y <= ry2) and (rx1 <= x <= rx2)
