import os
from PIL import Image
import numpy as np
import cv2
import pickle

base_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(base_dir, "images")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

#gloabal variable, lists, and set
current_id = 0
label_id = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(img_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            #print(label, path)

            if not label in label_id:
                label_id[label] = current_id
                current_id += 1

            id_ = label_id[label]
            print(label_id)
            #y_labels.append(label)
            #x_train.append(path)
            pil_img = Image.open(path).convert("L")#gray scale
            size = (550, 550)
            final_img = pil_img.resize(size, Image.ANTIALIAS)
            img_array = np.array(pil_img)
            
            #print(img_array)

            faces = face_cascade.detectMultiScale(img_array, scaleFactor = 1.5, minNeighbors = 5)
            for(x, y, h, w) in faces:
                roi = img_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)


#print(y_labels)
#print(x_train)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_id, f)

#saves the trained data to the yml file
recognizer.train(x_train, np.array(y_labels))
recognizer.save("src/trainner/face_trainner.yml")