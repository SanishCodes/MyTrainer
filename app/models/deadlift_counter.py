from .common import cv2, np, mp_pose, mp_drawing, calculate_angle, show_angle, show_counter

def DeadliftCounter():
    cap = cv2.VideoCapture(0)

    #curl counter variables
    counter = 0
    stage = None


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
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                
                
                #Calculate angle
                
                r_hip_angle = calculate_angle(r_shoulder, r_hip, r_knee)

                #Visualize angle
                show_angle(image,r_hip_angle,r_hip)


                if r_hip_angle > 160:
                    if stage == 'down':
                        counter+=1
                    stage='up'
                    
                
                if r_hip_angle<100 and stage=='up':
                    stage='down'
                    
                
                        
            except:
                pass

            box_color = (70, 130, 180)  

        
            cv2.rectangle(image, (10, 10), (300, 120), box_color, -1)
            
            # Draw REPS Label
            show_counter(image, counter)

            #Render Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(25,66,230), thickness=2, circle_radius=2))
            cv2.imshow('Deadlift Counter', image)
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            
                
    cap.release()
    cv2.destroyAllWindows()