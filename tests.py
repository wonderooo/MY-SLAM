import unittest
import cv2
import numpy as np

class TestOrb(unittest.TestCase):
    def setUp(self):
        pass
    def test_orb_create(self):
        orb = cv2.ORB_create()
        self.assertEqual(type(orb), cv2.ORB)
    def test_good_features(self):
        good = cv2.goodFeaturesToTrack(np.zeros((600, 400)).astype(np.uint8), 1, 1, 1)
        self.assertEqual(good, int)

if __name__ == '__main__':
    unittest.main()
