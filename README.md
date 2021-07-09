
# Face Recognition Attendance Tracking System [FaceRecAttTraSys] (FRATS)

**FRATS** is a very simple, commandline-based tool for tracking student's attendance. It was created and presented as my **Mini Project** at **Sikkim Manipal Institute of Technology.**

## Description

**FRATS** is a very simple attendance tracking system. It uses face-recognition to facilitate the process of taking attendance. Minimum human operation is required to run the program. It can reduce manual/proxy errors that occur using the traditional method of pen/paper. It stores the attendance logs as JSON files and converts them into PDF files and can email them to the respective lecturers. 

The project is still in it's initial stages and will be improved later on. Please view the to-do section to see what I will be working on.

## Getting Started

### Dependencies

So far, the program has been tested on Linux Mint 20.1 (Ulyssa). But since it was written in Python (which is an interpreted language), it should run on any platform that supports Python and has a webcam.

- **Operating System:** Linux/Windows/OSX
- **Languages:** Python3
- **Other Dependancies:** numpy, face_recognition, cv2 (OpenCV), json, fpdf, pdf_mail

A single line command to install them all:
```pip3 install numpy face_recognition cv2 json fpdf pdf_mail```

These are the only dependencies required to run the project. Python3 is recommended. It has not been tested on Python2, and may cause errors.

### Installing

Installing the project is very simple. Just clone the repository or download it:
```git clone https://github.com/jeezcalmdown88/FaceRecAttTrackSys/edit/main/README.md```

### Executing program

To run the project:
- Go to the project directory:
	```cd "Project Files"```
- Run:
		```python3 main.py```

If all the dependencies are installed, the program should start successfully in a few seconds.
