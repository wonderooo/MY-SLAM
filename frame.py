from array import array
import numpy as np
import cv2

class Frame(object):
    def __init__(self, frame: np.ndarray) -> None:
        self.frame = frame

    def extract(self, max_corners: int=3000, quality_level: float=0.01, min_distance: int=7) -> tuple:
        orb = cv2.ORB_create()
        features = cv2.goodFeaturesToTrack(np.mean(self.frame, axis=2).astype(np.uint8), max_corners, qualityLevel=quality_level, minDistance=min_distance)
        key_points = [cv2.KeyPoint(x=point[0][0], y=point[0][1], size=20) for point in features]
        key_points, descriptor = orb.compute(self.frame, key_points)
        return key_points, descriptor

    def process(self, kps: array):
        for kp in kps:
            self.frame = cv2.circle(self.frame, (int(kp.pt[0]), int(kp.pt[1])), 4, (0, 255, 0))
        return self.frame
