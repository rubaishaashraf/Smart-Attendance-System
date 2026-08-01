import cv2
import numpy as np
import os
import pickle
import time

video = cv2.VideoCapture(0)  

facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faces_data = []
TOTAL_IMAGES = 50

name = input("Enter name: ")

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to capture from camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        gray_face = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        resize_img = cv2.resize(gray_face, (50, 50))
        if len(faces_data) < TOTAL_IMAGES:
            faces_data.append(resize_img)
            time.sleep(0.2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.putText(frame, f"Images Captured: {len(faces_data)}/{TOTAL_IMAGES}", 
                    (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Capture Faces", frame)
    k = cv2.waitKey(1)
    if len(faces_data) >= TOTAL_IMAGES:
        break

video.release()
cv2.destroyAllWindows()

face_data = np.array(faces_data)
face_data = face_data.reshape(TOTAL_IMAGES, -1)

if not os.path.exists("data"):
    os.makedirs("data")

names_file = 'data/names.pkl'
if not os.path.exists(names_file):
    names = [name] * TOTAL_IMAGES
    with open(names_file, 'wb') as f:
        pickle.dump(names, f)
else:
    with open(names_file, 'rb') as f:
        names = pickle.load(f)
    names += [name] * TOTAL_IMAGES
    with open(names_file, 'wb') as f:
        pickle.dump(names, f)

faces_file = 'data/face_data.pkl'
if not os.path.exists(faces_file):
    with open(faces_file, 'wb') as f:
        pickle.dump(face_data, f)
else:
    with open(faces_file, 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, face_data, axis=0)
    with open(faces_file, 'wb') as f:
        pickle.dump(faces, f)

print(f"Saved {TOTAL_IMAGES} images for {name} successfully!")
