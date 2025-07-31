from common import cv2, np, mp_pose, mp_drawing, calculate_angle, show_angle

def BarbellRowCounter():
    cap = cv2.VideoCapture(0)

    #curl counter variables
    counter = 0
    stage = 'down'


    #Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence =0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor Image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            #Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            #Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                #Get Coordinates
                r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                #r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                r_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                r_hip_angle = calculate_angle(r_shoulder, r_hip, r_knee)

                #Visualize angle
                show_angle(image,r_hip_angle,r_knee)
                show_angle(image,r_elbow_angle,r_elbow)

                #Barbell Row Counter Logic
                #Check posture for barbell row
                if 40 < r_hip_angle <70:
                    if r_elbow_angle > 160 and stage == 'up':
                        stage = 'down'
                        counter+=1

                    if r_elbow_angle < 130 and stage == 'down':
                        stage = 'up'
                        
    
                        
            except:
                pass

            box_color = (70, 130, 180)  

        
            cv2.rectangle(image, (10, 10), (300, 120), box_color, -1)
            
            # Draw REPS Label
            cv2.putText(image, 'REPS', 
                        (20, 50),  # Top-left padding
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        (0, 0, 0), 2, cv2.LINE_AA)
            
            # Draw Counter Value
            cv2.putText(image, str(counter), 
                        (20, 100),  
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        2, 
                        (255, 255, 255), 4, cv2.LINE_AA)

            
        
            #Render Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(25,66,230), thickness=2, circle_radius=2))
            cv2.imshow('Barbell Row Counter', image)
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            
                
    cap.release()
    cv2.destroyAllWindows()