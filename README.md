# 🌟 Smart Attendance System
### Automating Attendance with Face Recognition

A smart attendance system that uses computer vision to detect faces and automatically record attendance in real time, improving efficiency and reducing manual effort.

---

## 🚀 Features
- Face detection using Haar Cascade  
- Face recognition using KNN algorithm  
- Real-time attendance marking  
- CSV-based attendance storage  
- Simple GUI interface  

---

## 🛠️ Tech Stack
- Python  
- OpenCV (cv2)  
- NumPy  
- Scikit-learn (KNeighborsClassifier)  
- Pickle (for model storage)  
- CSV (for attendance records)

---
  
## 📦 Install Libraries
``bash
pip install opencv-python numpy scikit-learn

---

## 📂 Project Structure
Smart-Attendance-System/
│
├── Attendance/        # Sample attendance records  
├── Dataset/           # Core project logic/code  
├── data/              # Trained model files (.pkl)  
├── haarcascade_frontalface_default.xml  
├── gui.py             # Main application  
├── README.md  

---

## ⚙️ How It Works (Step-by-Step)

1. Capture face data using webcam  
2. Store face images and labels  
3. Train KNN model on collected data  
4. Detect faces in real-time using OpenCV  
5. Predict identity using trained KNN model  
6. Record attendance with name and timestamp  
7. Save attendance in CSV file  

---

## ⚠️ Note
Attendance records and trained data are generated during runtime. Only sample data is included to maintain privacy.

---

## ▶️ Run
``bash
python gui.py


