

# Face Recognition

import cv2;     #openCV

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



# Computer Vision ..........................................
# Loading Haar Classifiers ......................


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); #global referential
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml'); #face referential
#smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml'); # face referential


# Origin Eye Coordinate

ox, oy, o_face_x = None, None, None;



# Detecting Face - Eyes

def detect(gray, frame):  

    
    # Detect face & get bound-coordinates 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5); #got {x,y,w,h}

    
    

    # Draw Face-Bounds on Frame

    for(x,y, w,h) in faces: 

        #enclose face in rect
        cv2.rectangle(frame,(x,y),(x+w+25, y+h+25),(255,105,180),5); 
        roi_gray = gray[y:y+h, x:x+int(w/2)];
        roi_color = frame[y:y+h, x:x+w]; #store face-coordinates (color)

        # Draw Line down Origin
        if(not(ox==None)):
            cv2.line(frame,(ox+o_face_x,0), (ox+o_face_x,800), (255,255,255),2)
        


        # Detect Eyes & get bound-coordinates 

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3);



        #set Origin position of eye

        global ox, oy, in_count, o_face_x;

        if(ox == None):

            for(ex,ey,ew,eh) in eyes[:1]:

                # Draw eye-enclosure
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 3) 
            
                # Draw midpoint of Eye-ROI
                mex = int(ex+ew/2);
                mey = int(ey+eh/2);
                cv2.circle(roi_color,(mex,mey),3,(0,255,0),3)

                # set Origin @ present coordinate
                if(cv2.waitKey(1) & 0xFF == ord('s')):
                    ox, oy = mex, mey
                    
                    o_face_x = x;
                    print ("\n\nOrigin Position: ", ox+o_face_x," , ",oy, "\n")
                    break;
                    

        # Measure EyE-displ. from origin
        if(not(ox==None)):

            for(ex,ey,ew,eh) in eyes[:1]:

            # Draw Origin Location
                # enclose eyes in rect 
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 3) 
                # Compute midpoint of Eye-ROI
                mex = int(ex+ew/2);
                mey = int(ey+eh/2);
                cv2.circle(roi_color,(mex,mey),3,(0,0,255),3)

               
                if(in_count % 17 == 0):      # frequency of motor-motion 
                    # move L
                    if(mex>ox):
                        move_left()
                        print("\nmoving left\nmex-:  ",mex+o_face_x,"\n")
                    # move R
                    elif(mex<ox):
                        move_right()
                        print("moving right\nmex:  ",mex+o_face_x,"\n")
                in_count+=1;
    return frame;





# Implementing Live Detection..........................

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

# Quit Webcam & Delete
video_capture.release()
cv2.destroyAllWindows()     