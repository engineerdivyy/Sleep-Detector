import cv2
import dlib
from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer

# --- Configuration ---
ALARM_FILE = "alarm.mp3" # Apni audio file ka naam yahan likhein
EYE_ASPECT_RATIO_THRESHOLD = 0.25 # Isse kam hua toh eyes closed maani jayengi
EYE_ASPECT_RATIO_CONSEC_FRAMES = 20 # Kitne frames tak eyes band rahein tab alarm baje

# --- Audio Setup ---
mixer.init()
mixer.music.load(ALARM_FILE)

# --- EAR Calculation Function ---
def eye_aspect_ratio(eye):
    # Vertical points ke beech ka distance
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    # Horizontal points ke beech ka distance
    C = distance.euclidean(eye[0], eye[3])
    
    # EAR Formula
    ear = (A + B) / (2.0 * C)
    return ear

# --- Dlib Setup ---
print("[INFO] Loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
# Make sure ye file same folder me ho
predictor = dlib.shape_predictor(r"C:\Users\yadav\OneDrive\Desktop\day 17\shape_predictor_68_face_landmarks.dat") 

# --- Left aur Right Eye ke indexes nikalo ---
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# --- Video Stream Start ---
cap = cv2.VideoCapture(0)
counter = 0 # Frames count karne ke liye
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (960, 720))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    rects = detector(gray, 0)
    
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        
        avgEAR = (leftEAR + rightEAR) / 2.0
        
        # --- Coordinates Calculate Karo (Dono ke liye alag variables) ---
        (l_x, l_y, l_w, l_h) = cv2.boundingRect(leftEye)
        (r_x, r_y, r_w, r_h) = cv2.boundingRect(rightEye)

        # --- Logic: Color Decide Karo ---
        # Default color Green hai
        eye_color = (0, 255, 0) 

        if avgEAR < EYE_ASPECT_RATIO_THRESHOLD:
            counter += 1

            # Agar Drowsiness Condition Meet ho gayi
            if counter >= EYE_ASPECT_RATIO_CONSEC_FRAMES:
                # Color RED kar do
                eye_color = (0, 0, 255)
                
                # Alarm Bajao (Loop mein)
                if not mixer.music.get_busy():
                    mixer.music.play(-1)
                
                # Screen Alert
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            counter = 0
            mixer.music.stop()
            # Color wapis Green ho jayega (kyunki loop wapis start hoga)

        # --- Ab Rectangle Draw Karo (Fixed Color ke saath) ---
        # Left Eye
        cv2.rectangle(frame, (l_x, l_y), (l_x + l_w, l_y + l_h), eye_color, 2)
        # Right Eye
        cv2.rectangle(frame, (r_x, r_y), (r_x + r_w, r_y + r_h), eye_color, 2)

    cv2.imshow("Sleep Detector", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()