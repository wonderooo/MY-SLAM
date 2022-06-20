import cv2
import numpy as np
from display import FeaturesPreview, Map3d
from frame import Frame
import multiprocessing as mp

def run(q):
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
            lordoza = list(map(lambda kp: (kp.pt[0], kp.pt[1]), kps))
            q.put(lordoza)
            display2d.draw(frame.process(kps))
        else:
            exit(0)
def run2(q):
    map3d = Map3d(q)
processes = []

if __name__ == '__main__':
    queue = mp.Queue()

    processes.append(mp.Process(target=run, args=(queue,)))
    processes.append(mp.Process(target=run2, args=(queue,)))
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
    
