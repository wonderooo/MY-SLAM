import cv2
import numpy as np

cap = cv2.VideoCapture("videos/0.hevc")

if cap.isOpened():
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS: ", fps)
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()
        features = cv2.goodFeaturesToTrack(gframe, 3000, qualityLevel=0.01, minDistance=7)
        kps = [cv2.KeyPoint(x=p[0][0], y=p[0][1], size=20) for p in features]
        kps, des = orb.compute(np.mean(frame, axis=2).astype(np.uint8), kps)
        print("orb: ", kps[0].pt[0], kps[1].pt)
        print("features: ", features[0][0][0], features[0][0][1])
        for kp in kps:
            frame = cv2.circle(frame, (int(kp.pt[0]), int(kp.pt[1])), 4, (0, 255, 0))
        cv2.imshow("my_SLAM", frame)
        key = cv2.waitKey(20)
        if key ==  ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
