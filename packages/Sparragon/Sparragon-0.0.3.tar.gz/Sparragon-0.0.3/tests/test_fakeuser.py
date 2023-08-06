import cv2
import sys, os

parentdir = os.path.realpath(os.path.join(os.path.dirname(__file__),os.pardir))
if parentdir not in sys.path:
    sys.path.insert(1, parentdir) # insert ../ just after ./

from sparragon import fakeuser

print(
    fakeuser.locateOnScreen(
        # cv2.imread("test_image.png"),
        cv2.imread("test_match.png", cv2.IMREAD_UNCHANGED),
        confidence=0.99
    )
)
