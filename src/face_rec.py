import os
import cv2 
import pickle
import _thread 
import time
import numpy as np 
from datetime import datetime

#cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

#creates error if the cascade is unavailable
if eye_cascade.empty():
  raise IOError('Unable to load the eye cascade classifier xml file')
if mouth_cascade.empty():
  raise IOError('Unable to load the mouth cascade classifier xml file')
if face_cascade.empty():
  raise IOError('Unable to load the face cascade classifier xml file')

#reads information from the trained data
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("src/trainner/face_trainner.yml")

labels = {"persons_name" : 1}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

#starts the capture on you usb camera
#if your using a laptop camera set it to 0
cap = cv2.VideoCapture(1)

#gets the current date to attach to the latest save file
time_date = datetime.now()
formated_time = time_date.strftime("%Y-%M-%H-%M-%S")
print("Current Time is: " + formated_time)
file_type = input("Would you like to save your video as a (.avi) , (.mp4) or (N)")

if file_type.lower() != "n":
    #checking if the file type is correct
    while file_type.lower() != ".mp4" and file_type.lower() != ".avi":
        print("Sorry the file type you entered is incorect")
        file_type = input("Would you like to save your video as a (.avi) or (.mp4)")

else:
    print("User is not recording...")

# #setting file destination
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

#set of usefull resolutions
std_dims =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

#method to get the fimentions
def get_dims(cap, res='1080p'):
    width, height = std_dims["480p"]
    if res in std_dims:
        width,height = std_dims[res]
    ## change the current caputre device
    ## to the resulting resolution
    custom_res(cap, width, height)
    return width, height


#posible file types that the video could be saved in
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
# changes the video resolution depending on what u need



#Global Variables
color = {'Black' : (0, 0, 0), 'Red' : (0, 0, 255), 'Green' : (0, 255, 0), 'Blue' : (255, 0, 0)} 
name = ['Eye', 'Mouth', 'Face', 'Mask-ON', 'Mask-OFF', 'Not Detected']
eye_detected = False
face_detected = False
person_rec = False
rec_name = 'Not Identified'
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
def face_detector(returning = 'face_detected'):
    for(x ,y, h, w) in faces:
        stroke = 2
        roi_gray = gray[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)
        
        person_rec = True
        rec_name = labels[id_]
        
        cv2.rectangle(frame, (x , y), (x + w, y + h), box_color, stroke)
        face_detected = True
        #print('---------RETURNING: ' + str(returning))
        return eval(returning)
    
    face_detected = False
    person_rec = False
    rec_name = 'Not Indentified'
    #print('---------RETURNING: ' + str(returning))
    return eval(returning)

        
#Mouth Function
def mouth_detector():
    for(x ,y, h, w) in mouths:
        stroke = 2
        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)
        if conf > 120:
            cv2.rectangle(frame, (x , y), ((x + h), (y + w)), (255,0,0), stroke)
        mouth_detected = True
        return mouth_detected
    
    mouth_detected = False
    return mouth_detected

#Multi threading allows the program to run 
#multiple things at once ex: 2 for loops at the same time
def multi_threading():
    _thread.start_new_thread(eye_detector, ()) 
    _thread.start_new_thread(face_detector, ()) 
    #_thread.start_new_thread(mouth_detector, ()) 

#Live Video Capture Starts
while True:
    ret, frame = cap.read()

    #sets the gray scale and cascade variables
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mouths = mouth_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 3)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 3)

    #sets the return of each function into a variable
    eye_val = eye_detector()
    face_val = face_detector('face_detected')
    person_val = face_detector('person_rec')
    name_val = face_detector('rec_name')
    # mouth_val = mouth_detector()

    multi_threading()

    #outputs for debuging
    # print('EYE: ' + str(eye_val))
    # print('Face: ' + str(face_val))
    # print('Person: ' + str(person_val))
    # print('Name: ' + str(name_val))
    # print(mouth_val) wasnt used orginaly

    font = cv2.FONT_HERSHEY_SIMPLEX
    face_color = (255, 0, 0) #Blue
    stroke = 2
    text_pos = (50, 50)
    user_pos = (450, 50)

    if(face_val == True and eye_val == True):
        #print('MASK-OFF')
        box_color = (0, 0, 255) #Red
        cv2.putText(frame, name[4], text_pos, font, 1, color['Red'], stroke, cv2.LINE_AA)
    if(face_val == False and eye_val == True):
        #print('MASK-ON')
        box_color = (0, 255, 0) #Green
        cv2.putText(frame, name[3], text_pos, font, 1, color['Green'], stroke, cv2.LINE_AA)

    #shows the recognised persons name on the frame
    if(person_val == True):
        #print('----------------')
        cv2.putText(frame, name_val, user_pos, font, 1, color['Black'], stroke, cv2.LINE_AA)

    out.write(frame)

    #Pressing Escape Key will quit the program
    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == 27:
        print('User Exited...')
        break

    #time.sleep(0.01)

#stops the capture
cap.release()
out.release()
cv2.destroyAllWindows()

