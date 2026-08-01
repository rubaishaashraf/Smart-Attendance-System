import cv2
import numpy as np
import os
import csv
import time
import pickle

from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime


video=cv2.VideoCapture(0) #0 for webcam
facedetect=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


with open('data/names.pkl','rb') as w:
    LABELS=pickle.load(w)
    
with open('data/face_data.pkl','rb') as f:
    FACES=pickle.load(f)
    
    
knn=KNeighborsClassifier(n_neighbors=5)
print("Faces:", FACES.shape)
print("Labels:", len(LABELS))
knn.fit(FACES,LABELS)


imagebackground=cv2.imread("bg.png")

COL_NAMES=['NAME','TIME']


if not os.path.exists("bg.png"):
    ret, bg_frame = video.read()
    if ret:
        cv2.imwrite("bg.png", bg_frame)
        print("Background captured and saved as bg.png")

imagebackground = cv2.imread("bg.png")


while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray,1.3,5)
    
    for (x,y,w,h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        gray_face = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        resized_img = cv2.resize(gray_face, (50,50)).flatten().reshape(1, -1)

        
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        
        timeStamp=datetime.fromtimestamp(ts).strftime('%H:%M-%S')
        if not os.path.exists("Attendance"):
            os.makedirs("Attendance")
        exit=os.path.isfile('Attendance/Attendance_'+date+'.csv')
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        cv2.putText(frame,str(output[0]),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,255,255),2)
        attendance=[str(output[0]),str(timeStamp)]
    bg_h, bg_w, _ = imagebackground.shape
    slot_y, slot_x = 162, 55
    slot_h = bg_h - slot_y
    slot_w = bg_w - slot_x
    frame_resized = cv2.resize(frame, (slot_w, slot_h))
    imagebackground[slot_y:slot_y+slot_h, slot_x:slot_x+slot_w] = frame_resized




    cv2.imshow("Frame",imagebackground)
    k=cv2.waitKey(1)
    if k== ord('o'):
        time.sleep(5)
        
        if exit:
            with open('Attendance/Attendance_'+date+'.csv','a') as cvsfile:
                writer=csv.writer(cvsfile)
                writer.writerow(attendance)
            cvsfile.close()
            
        else:
            with open('Attendance/Attendance_'+date+'.csv','w') as cvsfile:
                writer=csv.writer(cvsfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            cvsfile.close()
            
    if k==27:
        break
    
video.release()
cv2.destroyAllWindows()
                
    