import cv2
import numpy as np
import mediapipe as mp
from utils import calculate_angle, show_angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose