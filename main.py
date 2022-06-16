import cv2
import numpy as np
from display import FeaturesPreview
from frame import Frame


if __name__ == '__main__':
    cap = cv2.VideoCapture("videos/0.hevc")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    display2d = FeaturesPreview(width, height)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = Frame(np.array(frame))
            kps, des = frame.extract()
            display2d.draw(frame.process(kps))
        else:
            exit(0)
        print('after')
