import numpy as np
import cv2


def calculate_angle(a, b, c):
    """
    Calculates the angle (in degrees) formed at point 'b' by the vectors ab and cb.

    Parameters:
    - a: The first point (before the joint), as a list or array of [x, y].
    - b: The central point (joint) where the angle is formed.
    - c: The third point (after the joint), as a list or array of [x, y].

    Returns:
    - angle: The absolute angle in degrees between the vectors (range: 0° to 180°).
    """
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = round(np.abs(radians * 180.0 / np.pi),0)
    return 360 - angle if angle > 180 else angle




def show_angle(image, angle, reference_point):
    """
    Draws the given angle value on the image at a specified reference point.

    Parameters:
    - image: The OpenCV image/frame on which to overlay the angle.
    - angle: The angle value (in degrees) to display.
    - reference_point: A 2D point (x, y) in normalized coordinates (0–1 range) 
                       relative to image width and height, where the angle text should appear.

    Returns:
    - None (modifies the image in-place)
    """

    cv2.putText(image, str(angle),
                        tuple(np.multiply(reference_point, [1920,1080]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 6, cv2.LINE_AA)
    

def show_counter(image, counter):
    """
    Draws a counter box with the label 'REPS' and the counter value.
    
    Parameters:
    - image: the OpenCV image frame
    - counter: the number to display
    - box_color: the background color of the counter box (default: steel blue)
    
    Returns:
    - image: the modified image with counter overlay
    """
     
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