import numpy as np 
import cv2 

cap = cv2.VideoCapture(1)

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

def custom_res(width , height):
    cap.set(3, width)
    cap.set(4, height)


make_720p()

while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)

    #Pressing Q qill quit the program
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()