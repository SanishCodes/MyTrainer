from .common import cv2, np, mp_pose, mp_drawing, calculate_angle, show_angle, show_counter

def CrunchCounter():
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
                r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                #Calculate angle
                
                r_hip_angle = calculate_angle(r_shoulder, r_hip, r_knee)
                floor_y = r_hip[1]
                #Visualize angle & Counter
                show_angle(image,r_hip_angle,r_hip)
                show_counter(image, counter)

                cv2.putText(image, f"DIF: {str(abs(r_ankle[1] - floor_y))}", 
                (20, 250), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (0, 0, 0), 2, cv2.LINE_AA)


                # Crunch Counter Logic
                # Check if the right foot is close to the estimated floor level (i.e., in contact with the ground)
                if(abs(r_ankle[1] - floor_y)<0.1):
                    if r_hip_angle > 135:
                        stage='down'

                    if r_hip_angle<120 and stage=='down':
                        stage='up'
                        counter+=1
        
            except:
                pass

            
            

            #Render Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(25,66,230), thickness=2, circle_radius=2))
            cv2.imshow('Crunch Counter', image)
                
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            
                
    cap.release()
    cv2.destroyAllWindows()