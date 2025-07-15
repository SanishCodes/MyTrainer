from .common import cv2, np, mp_pose, mp_drawing, calculate_angle, show_angle

def SquatsCounter():
    cap = cv2.VideoCapture(1)

    #curl counter variables
    counter = 0
    stage = 'up'


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
                r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                #Calculate angle
                
                r_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)

                #Visualize angle
                show_angle(image,r_knee_angle,r_knee)


                #Curl Counter logic
                
                
                
                if r_knee_angle > 82 and stage=='down':
                    stage='up'
                    counter+=1
                
                if r_knee_angle<75 and stage=='up':
                    stage='down'
                    
                
                        
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
            cv2.imshow('Squats Counter', image)
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            
                
    cap.release()
    cv2.destroyAllWindows()