import cv2
import numpy as np
import face_recognition
import time
from pathlib import Path
import os

database_path = "./database"
admin_password = "PASSWORD"

print("~ Welcome to the FaceRecAttTrackSys (FRATS) ~")
while True:
	print("\nOptions: \n")
	print("1. Train Model")
	print("2. New Session")
	print("3. Quit")
	choice = int(input("\nEnter option> "))

	if choice == 1:
		print("1. Train from camera (videostream).")
		print("2. Train from pictures.")
		choice = int(input("Enter option> "))
		print()

		if choice == 1:
			print("1. Training from Videostream\n")
			print("Instructions:")
			print("\t1. Check if:")
			print("\t\t1. Lighting is proper.")
			print("\t\t2. Student is looking straight and face is shown clearly.")
			print("\t\t3. A red rectangle is around the face - it means the face has been detected.")
			print("\t2. If the above conditions match, press 'c' to capture image.")
			print("\t3. Wait 5 seconds for image to get stored in the database.")
			print()

			name_of_class = '-'.join(input("Class name? ").split())

			if not os.path.exists(database_path + "/" + name_of_class):
				os.mkdir(database_path + "/" + name_of_class)
				number_of_students = int(input("Number of Students? "))
			else:
				print("Class already exists.")
				if input(("Do you want to add new students? (Y/N) ")).lower() == 'y':
					number_of_students = int(input("Number of Students? "))
				else:
					continue

			for i in range(0, number_of_students):
				name_of_student = input("Enter student {} name: ".format(i + 1))

				video = cv2.VideoCapture(0)
				width = int(video.get(3))
				height = int(video.get(4))

				while True:
					ret, frame = video.read()
					image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
					faceLoc = face_recognition.face_locations(image)

					for top, right, bottom, left in faceLoc:
						cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

					cv2.rectangle(image, (10, 10), (width - 10, height - 10), (255, 0, 0), 2)
					cv2.imshow('image', image)

					if cv2.waitKey(1) & 0xFF == ord('c'):
						# Save the capture and move to next student
						print("Model trained for student '{}'.".format(name_of_student))
						cv2.imwrite(database_path + "/" + name_of_class + "/" + '-'.join(name_of_student.split()) + '.jpg', frame)
						break
				
				video.release()
				cv2.destroyAllWindows()
			print("Model trained for class {}.".format(name_of_class))

		elif choice == 2:
			print("2. Training from Pictures\n")
			print("Instructions:")
			print("\t1. Make a folder in the Database Path.")
			print("\t\tCurrent Database Path: " + database_path)
			print("\t2. Name the folder the name of the class.")
			print("\t3. Add the pictures of all the students of the class, labelled properly.")

	elif choice == 2:
		print("Starting new session...")
		print("Select class: ")
		for i in range(len(os.listdir(database_path))):
			print("[{}] {}".format(i, os.listdir(database_path)[i]))

		try:
			index = int(input("Index? "))
		except:
			print("Invalid class index. Select from list.")

	elif choice == 3:
		print("Bye.")
		quit()

	else:
		print("Invalid choice.")