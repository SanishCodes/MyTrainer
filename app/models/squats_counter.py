from .common import cv2, np, mp_pose, mp_drawing, calculate_angle, show_angle, show_counter
from .pose_tracker import PoseLandmarkTracker
import time

def SquatsCounter():
    last_warning_time = 0
    warning_message = []
    depth_warning_given = False
    back_warning_given = False
    toe_warning_given = False
    tracker = PoseLandmarkTracker()
    
    #curl counter variables
    counter = 0
    stage = None
    descending = False
    min_knee_angle=360
    min_back_angle=360
    max_knee_forward = -1
    margin = 0.02

    while True:
        image, raw_landmarks, landmarks = tracker.get_frame_data()
        if image is None or not landmarks:
            continue

        try:
            r_shoulder = landmarks['RIGHT_SHOULDER']
            r_hip = landmarks['RIGHT_HIP']
            r_knee = landmarks['RIGHT_KNEE']
            r_ankle = landmarks['RIGHT_ANKLE']
            
            r_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
            r_hip_angle = calculate_angle(r_shoulder, r_hip, r_knee)


            #show_angle(image, r_knee_angle, r_ankle)
            #show_angle(image, min_knee_angle, r_shoulder)

            try:
                cv2.putText(image, f"Min Angle={min_knee_angle}", 
                (20, 90),  # Top-left padding
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                (0, 0, 0), 2, cv2.LINE_AA)
            except:
                pass
            #show_angle(image, r_hip_angle, r_hip)
            show_angle(image, r_knee[0] - r_ankle[0], r_knee)
            # Start going down
            if r_knee_angle < 140 and not descending:
                descending = True
                min_knee_angle = r_knee_angle
                min_back_angle = r_hip_angle
                stage = 'down'
            
            # While going down, keep tracking lowest angle
            if descending:
                min_knee_angle = min(min_knee_angle, r_knee_angle)
                min_back_angle = min(min_back_angle, r_hip_angle)
                max_knee_forward = max(max_knee_forward, r_knee[0])
            '''
            if descending and r_knee_angle < min_knee_angle:
                min_knee_angle = r_knee_angle
              
            if descending and r_hip_angle < min_back_angle:
                min_back_angle = r_hip_angle

            if descending:
                max_knee_forward = max(max_knee_forward, r_knee[0])
            '''
            # When user stands up fully
            if r_knee_angle > 170 and descending:
                counter += 1

                # Check squat depth form
                if not depth_warning_given:
                    if 130 <= min_knee_angle < 140:
                        warning_message.append("Go deeper next time!")
                        last_warning_time = time.time()
                        depth_warning_given = True

                    elif min_knee_angle < 110:
                        warning_message.append("Too deep! Protect your knees")
                        last_warning_time = time.time()
                        depth_warning_given = True
                
                margin = 0.02  # small tolerance
                
                if not toe_warning_given:
                    if (max_knee_forward - r_ankle[0]) > margin:
                        warning_message.append("Right knee past toe!")
                        last_warning_time = time.time()
                        toe_warning_given = True

                if not back_warning_given:
                   
                    if min_back_angle < 90:
                        warning_message.append('Straighten your back') 
                        last_warning_time = time.time()
                        back_warning_given = True
              

                # Reset states
                depth_warning_given = False
                back_warning_given = False
                toe_warning_given = False
                descending = False
                
                min_knee_angle = 999
                stage = 'up'
                
                
    

            

            
            if warning_message and time.time() - last_warning_time < 2:
                y_position = 300
                for msg in warning_message:
                    cv2.putText(image, msg, 
                    (20, y_position),  # Top-left padding
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, 
                    (0, 0, 0), 2, cv2.LINE_AA)
                    y_position += 50
                
            else:
                warning_message.clear()
            
            
        except KeyError as e:
            print(f"Missing landmark: {3}")
        
        show_counter(image, counter)
        tracker.draw_landmarks(image, raw_landmarks)
        cv2.imshow('Squats Counter', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    tracker.release()
    