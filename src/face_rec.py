import os
import numpy as np 
import cv2 
from datetime import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
cap = cv2.VideoCapture(1)

time = datetime.now()
formated_time = time.strftime("%Y-%M-%H-%M-%S")
print("Current Time is: " + formated_time)
file_type = input("would you like to save your video as a (.avi) or (.mp4)")

#checking if the file type is correct
while file_type != ".mp4" and file_type != ".avi":
    print("Sorry the file type you entered is incorect")
    file_type = input("would you like to save your video as a (.avi) or (.mp4)")

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






























while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    
    for(x ,y, h, w) in faces:
        print(x ,y, h, w)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        img_item = "images/mohammad.png"
        cv2.imwrite(img_item, roi_gray)
        
        face_color = (255, 0, 0) #BGR
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x , y), (end_cord_x, end_cord_y), face_color, stroke)

    out.write(frame)
    #Pressing Q qill quit the program
    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#stops capture
cap.release()
out.release()
cv2.destroyAllWindows()