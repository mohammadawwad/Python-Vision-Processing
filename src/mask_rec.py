import os
import cv2 
import pickle
import _thread 
import numpy as np 
from datetime import datetime

#cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

if eye_cascade.empty():
  raise IOError('Unable to load the eye cascade classifier xml file')
if mouth_cascade.empty():
  raise IOError('Unable to load the mouth cascade classifier xml file')
if face_cascade.empty():
  raise IOError('Unable to load the face cascade classifier xml file')

cap = cv2.VideoCapture(1)

time = datetime.now()
formated_time = time.strftime("%Y-%M-%H-%M-%S")
print("Current Time is: " + formated_time)
file_type = input("Would you like to save your video as a (.avi) , (.mp4) or (N)")

if file_type.lower() != "n":
    #checking if the file type is correct
    while file_type.lower() != ".mp4" and file_type.lower() != ".avi":
        print("Sorry the file type you entered is incorect")
        file_type = input("Would you like to save your video as a (.avi) or (.mp4)")

else:
    print("User is not recording...")
    
#setting file destination
file_destination = 'code/videos/'
filename = file_destination + formated_time + "-" + "video" + file_type
fps = 24.0
res = "480"
#use ffmpeg for audio recording

#changes the video resolution depending on what u need
def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1080)

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

def custom_res(cap, width , height):
    cap.set(3, width)
    cap.set(4, height)


std_dims =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

def get_dims(cap, res='1080p'):
    width, height = std_dims["480p"]
    if res in std_dims:
        width,height = std_dims[res]
    ## change the current caputre device
    ## to the resulting resolution
    custom_res(cap, width, height)
    return width, height

video_type = {
    'avi' : cv2.VideoWriter_fourcc(*'XVID'),
    'mp4' : cv2.VideoWriter_fourcc(*'XVID'),
}

def get_vid_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in video_type:
        return video_type[ext]
    return video_type['avi']

#setting capture to 480p
make_480p()
video_type_cv2 = get_vid_type(filename)
out = cv2.VideoWriter(filename, video_type_cv2, fps, get_dims(cap, res), True)

#Global Variables
name = ['Eye', 'Mouth', 'Face', 'Mask-ON', 'Mask-OFF', 'Not Detected']
eye_detected = False
face_detected = False
mouth_detected = False
box_color = (255, 0, 0) #Blue

#Eye Function
def eye_detector():
    for(x ,y, h, w) in eyes:
        stroke = 2
        cv2.rectangle(frame, (x , y), (x + w, y + h), box_color, stroke)
        eye_detected = True
        return eye_detected
    eye_detected = False
    return eye_detected

#Face Function
def face_detector():
    for(x ,y, h, w) in faces:
        stroke = 2
        cv2.rectangle(frame, (x , y), (x + w, y + h), box_color, stroke)
        face_detected = True
        return face_detected
    
    face_detected = False
    return face_detected

#Mouth Function
def mouth_detector():
    for(x ,y, h, w) in mouths:
        stroke = 2
        cv2.rectangle(frame, (x , y), ((x + h), (y + w)), (255,0,0), stroke)
        mouth_detected = True
        return mouth_detected
    
    mouth_detected = False
    return mouth_detected

def multi_threading():
    _thread.start_new_thread(eye_detector, ()) 
    _thread.start_new_thread(face_detector, ()) 
    #_thread.start_new_thread(mouth_detector, ()) 

#Live Video Capture Starts

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mouths = mouth_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 3)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 3)

    eye_val = eye_detector()
    face_val = face_detector()
    mouth_val = face_detector()

    multi_threading()

    print(eye_val)
    print(face_val)
    print(mouth_val)

    font = cv2.FONT_HERSHEY_SIMPLEX
    face_color = (255, 0, 0) #Blue
    color = {'Black' : (0, 0, 0), 'Red' : (0, 0, 255), 'Green' : (0, 255, 0), 'Blue' : (255, 0, 0)}        #Black
    stroke = 2
    text_pos = (50, 50)

    if(face_val == True and eye_val == True):
        print('DISPLAYING FASLE')
        box_color = (0, 0, 255) #Red
        cv2.putText(frame, name[4], text_pos, font, 1, color['Red'], stroke, cv2.LINE_AA)
    if(face_val == False and eye_val == True):
        print('DISPLAYING TRUE')
        box_color = (0, 255, 0) #Green
        cv2.putText(frame, name[3], text_pos, font, 1, color['Green'], stroke, cv2.LINE_AA)

    out.write(frame)
    #Pressing Escape Key will quit the program
    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == 27:
        print('User Exited...')
        break

#stops capture and video recording
cap.release()
out.release()
cv2.destroyAllWindows()