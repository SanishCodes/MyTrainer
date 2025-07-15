import numpy as np
import cv2

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

def show_angle(image, angle, reference_point):
    cv2.putText(image, str(angle),
                        tuple(np.multiply(reference_point, [1920,1080]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 6, cv2.LINE_AA)