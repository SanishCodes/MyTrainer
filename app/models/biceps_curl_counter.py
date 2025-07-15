
from .common import cv2, np, mp_pose, mp_drawing, calculate_angle


def BicepCurlCounter():
    cap = cv2.VideoCapture(1)

    counter = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Left arm
                l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Right arm
                r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Angles
                l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
                r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

                # Curl counter logic
                if l_angle > 160 and r_angle > 160:
                    stage = 'down'
                if l_angle < 30 and r_angle < 30 and stage == 'down':
                    stage = 'up'
                    counter += 1

                # Show angles
                cv2.putText(image, f'{int(l_angle)}',
                            tuple(np.multiply(l_elbow, [image.shape[1], image.shape[0]]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                cv2.putText(image, f'{int(r_angle)}',
                            tuple(np.multiply(r_elbow, [image.shape[1], image.shape[0]]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

            except:
                pass

            # Rep counter box
            cv2.rectangle(image, (10, 10), (300, 120), (70, 130, 180), -1)
            cv2.putText(image, 'REPS', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, str(counter), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)

            # Draw pose landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(25,66,230), thickness=2, circle_radius=2))

            cv2.imshow('Biceps Curl Counter', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


