import cv2 
import mediapipe as mp


class PoseLandmarkTracker:
    def __init__(self,  cam_index=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.cap = cv2.VideoCapture(cam_index)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.landmark_names = self.mp_pose.PoseLandmark

    def get_frame_data(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None, {}
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        landmark_dict = {}
        if results.pose_landmarks:
            for lm in self.landmark_names:
                landmark = results.pose_landmarks.landmark[lm.value]
                landmark_dict[lm.name] = [landmark.x, landmark.y]
        
        return image, results.pose_landmarks, landmark_dict
    
    def draw_landmarks(self, image, landmarks):
        if landmarks:
            self.mp_drawing.draw_landmarks(
                image, landmarks, self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(25,66,230), thickness=2, circle_radius=2)
            )

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()