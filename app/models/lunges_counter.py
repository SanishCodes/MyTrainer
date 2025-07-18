from .common import cv2, np, mp_pose, mp_drawing, calculate_angle, show_angle

def LungesCounter():
    cap = cv2.VideoCapture(0)

    #curl counter variables
    l_counter = 0
    l_stage = None

    r_counter = 0
    r_stage = None


    #Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence =0.8, min_tracking_confidence=0.8) as pose:
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
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                

                floor_y = max(l_ankle[1], r_ankle[1])
                
                
                if(abs(r_knee[1] - floor_y) < 0.08):
                    l_stage='down'


                if(abs(r_knee[1] - floor_y) > 0.1) and l_stage=='down':
                    l_stage='up'
                    l_counter+=1
                
                if(abs(l_knee[1] - floor_y) < 0.08):
                    r_stage='down'

                if(abs(l_knee[1] - floor_y) > 0.1) and r_stage=='down':
                    r_stage='up'
                    r_counter+=1
 
            except:
                pass

            box_color = (70, 130, 180)  

            
            cv2.rectangle(image, (10, 10), (300, 120), box_color, -1)
            cv2.putText(image, f"Left-Stage: {l_stage} \n Right-Stage: {r_stage}", (20,300),cv2.FONT_HERSHEY_COMPLEX,2,cv2.LINE_AA)
            
            # Draw REPS Label
            cv2.putText(image, 'L-REPS      R-REPS', 
                        (20, 50),  # Top-left padding
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        (0, 0, 0), 2, cv2.LINE_AA)
            
            # Draw Counter Value
            cv2.putText(image, f"{str(l_counter)}   {str(r_counter)}", 
                        (20, 100),  
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        2, 
                        (255, 255, 255), 4, cv2.LINE_AA)
            
          
        
            #Render Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(25,66,230), thickness=2, circle_radius=2))
            cv2.imshow('Lunges Counter', image)
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            
                
    cap.release()
    cv2.destroyAllWindows()