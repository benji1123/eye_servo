
# Face Recognition

import cv2;         #openCV
import argparse;

# arduino stuffs ........................................

import serial   #interface -> Arduino
import time

PORT = "COM3"
RATE = 9600
MOVE_LEFT  = 'l'
MOVE_RIGHT = 'r'

# Establish Servo-Cnxn & Controls
def move_left():
    if(connected):
        ser.write(MOVE_LEFT.encode())
def move_right():
    if(connected):
        ser.write(MOVE_RIGHT.encode())
connected = False
ser = serial.Serial(PORT, RATE)

while(not(connected)):
    serin = ser.read()
    connected = True

in_count = 0


# Arguments Stuffs .........................................
parser = argparse.ArgumentParser(description = 'python main.py [opaque][1]')
parser.add_argument("bgrnd",help="0=>clear bgrnd, 1=>opaque bgrnd",type=int)
args = parser.parse_args()


# Computer Vision ..........................................
# Loading Haar Classifiers 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); #global referential
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml'); #face referential
#smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml'); # face referential



# Origin Eye Coordinate
ox, oy, o_face_x = None, None, None;

# Detecting Face - Eyes
def detect(gray, frame):  

    cv2.rectangle(frame,(0,0),(0,5),(255,0,0),5);


    global args;
    # Detect face & get bound-coordinates 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5); #got {x,y,w,h}
    
    if(args.bgrnd==1):
        cv2.rectangle(frame,(0,0),(1000, 1000),(255,105,180),10000); 
    
    
    # Draw Face-Bounds on Frame

    for(x,y, w,h) in faces: 

        #enclose face in rect
        cv2.rectangle(frame,(x,y),(x+w+25, y+h+25),(255,105,180),5); 
        roi_gray = gray[y:y+h, x:x+int(w/2)];
        roi_color = frame[y:y+h, x:x+w]; #store face-coordinates (color)

        # Draw Line down Origin
        if(not(ox==None)):
            cv2.line(frame,(ox+o_face_x,0), (ox+o_face_x,800), (255,255,255),3)
        

        # Detect Eyes & get bound-coordinates 
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1,3);


        #SET ORIGIN POSITION of EyE
        global ox, oy, in_count, o_face_x;

        if(ox == None):
            for(ex,ey,ew,eh) in eyes[:1]:
                # Draw eye-enclosure
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 3) 
            
                # Draw midpoint of Eye-ROI
                mex, mey = int(ex+ew/2), int(ey+eh/2);
                cv2.circle(roi_color,(mex,mey),3,(0,255,0),5)

                # set Origin @ present coordinate
                if(cv2.waitKey(1) & 0xFF == ord('s')):
                    ox, oy = mex, mey
                    o_face_x = x;
                    print ("\n\nOrigin Position: ", ox+o_face_x," , ",oy, "\n")
                    break;
                    

        # Measure DISPLACEMENT from ORIGIN
        if(not(ox==None)):

            for(ex,ey,ew,eh) in eyes[:1]:
            
            # Draw Origin for Visual Refernece 
                cv2.rectangle(roi_color, (ex, ey), 
                             (ex+ew, ey+eh), (0, 255, 0), 3)      # Draw outer eyes-bound 
                mex, mey = int(ex+ew/2), int(ey+eh/2);           # Compute MIDPOINT of Eye
                cv2.circle(roi_color,(mex,mey),3,(0,0,255),3)     # Draw Midpoint


                # INTERFACE with SERVOMOTOR
                cv2.rectangle(frame, (ox+o_face_x, oy), 
                             (ox+o_face_x, oy+50), (0, 255, 0), 3)

                if(in_count % 17 == 0):       
                    
                    # move L 
                    if(mex>ox):
                        move_left()
                        print("\nmoving left\nmex-:  ",mex+o_face_x,
                            "\nox: ",ox+o_face_x)
                    
                    # move R 
                    elif(mex<ox):
                        move_right()
                        print("moving right\nmex:  ",mex+o_face_x,
                            "\nox: ",o_face_x)
                
                in_count+=1;
    
    return frame;




# Implementing Continuous Detection with Webcam..........................

video_capture = cv2.VideoCapture(0);    #"0" => object of live webcam video
while True:

    
    # sending latest frame from cam => detect()
    _, frame = video_capture.read();   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); #cascade operates on grayscale
    canvas = detect(gray,frame); 


    # un-invert camera-feed
    canvas = cv2.flip(canvas, 1)


    # resizing webcam window
    cv2.namedWindow('Press Q to Quit',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Press Q to Quit',800,620)
    cv2.imshow('Press Q to Quit',canvas);
    
    if cv2.waitKey(1) & 0xFF == ord('q'):   #quit on "q" press
        break;


# Quit Webcam & Close Elements
video_capture.release()
cv2.destroyAllWindows()     