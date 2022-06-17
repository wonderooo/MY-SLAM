import cv2
import numpy as np
from display import FeaturesPreview
from frame import Frame


if __name__ == '__main__':
    cap = cv2.VideoCapture("videos/0.hevc")
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    display2d = FeaturesPreview(width, height, fps)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = Frame(np.array(frame))
            kps, des = frame.extract()
            display2d.draw(frame.process(kps))
        else:
            exit(0)
