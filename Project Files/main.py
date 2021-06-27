import cv2
import numpy as np
import face_recognition
import time
from pathlib import Path
import os, json, datetime
import pdf_generator
import log_sender

database_path = "./database"
admin_password = "PASSWORD"

def recognize_face(encode_reference):
	video = cv2.VideoCapture(0)
	width = int(video.get(3))
	height = int(video.get(4))

	return_output = False

	while True:
		ret, frame = video.read()
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		faceLoc = face_recognition.face_locations(image)

		for top, right, bottom, left in faceLoc:
			cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

		cv2.rectangle(image, (10, 10), (width - 10, height - 10), (255, 0, 0), 2)
		cv2.imshow('image', image)

		keypress = cv2.waitKey(1)

		if keypress == ord('c'):
			# Save the capture and move to next student
			cropped_image = frame[top:bottom, left:right]

			if faceLoc:
				try:
					encode_capture = face_recognition.face_encodings(cropped_image)[0]
				except:
					print("Error encoding face. Try again.")
					continue

				results = face_recognition.compare_faces([encode_reference], encode_capture)[0]
				faceDis = face_recognition.face_distance([encode_reference], encode_capture)

				print("{}% match...".format(100 - faceDis * 100))

				if results and faceDis < 0.500:
					print("Present.")
					return_output = True
					break
				else:
					print("Student not matched. Try again.")
					continue

			else:
				print("Face cannot be detected. Try again.")
				continue

			break

		elif keypress == ord('q'):
			print("Absent.")
			return_output = False
			break
	
	video.release()
	cv2.destroyAllWindows()
	return return_output

def train_from_videostream(name_of_class, registration_number, name_of_student):
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
			
			cropped_image = frame[top:bottom, left:right]

			if faceLoc:
				if face_recognition.face_encodings(cropped_image):
					cv2.imwrite(database_path + "/" + name_of_class + "/student_images/" + registration_number + "-" + name_of_student + '.jpg', cropped_image)
					print("Image captured for student '{}'.".format(name_of_student))
					break
				else:
					print("Error encoding face. Try again.")

			else:
				print("Face cannot be detected. Try again.")
				continue

	
	video.release()
	cv2.destroyAllWindows()

def input_subjects():
	subject_list = []

	while True:
		number_of_subjects = int(input("Number of subjects? "))
		if number_of_subjects >= 1:
			break

	for i in range(number_of_subjects):
		print("Subject [{}]:-".format(i + 1))
		subject_name = input("\tSubject Name? ").upper()
		subject_teacher = input("\tSubject Teacher? ").upper()
		teacher_email = input("\tTeacher's Email? ")

		subject_list.append((subject_name, subject_teacher, teacher_email))

	return subject_list


def build_subject_list(name_of_class):
	if not os.path.exists(database_path + "/" + name_of_class + "/subject_list.json"):
		print("Subject list does not exist. Creating a new one...")
		subject_list = input_subjects()
		json_string = json.dumps(subject_list)
		json_file = open(database_path + "/" + name_of_class + "/subject_list.json", "w")
		json_file.write(json_string)
		json_file.close()

		print("Subject list updated.")

	else:
		if input("Subject list already exists. Add new subjects? (Y/N) ").upper() == 'Y':
			json_file = open(database_path + "/" + name_of_class + "/subject_list.json", "r")
			json_content = json_file.read()
			old_subject_list = json.loads(json_content)

			json_file.close()

			subject_list = input_subjects()
			old_subject_list.extend(subject_list)

			json_string = json.dumps(old_subject_list)
			json_file = open(database_path + "/" + name_of_class + "/subject_list.json", "w")
			json_file.write(json_string)
			json_file.close()

			print("Created new subject list.")

class AttendanceLog:
	def __init__(self, name_of_class, subject, attendance_list):
		self.name_of_class = name_of_class
		self.subject = subject
		self.attendance_list = attendance_list
		self.date = datetime.date.today().strftime("%d:%m:%Y")
		self.time = datetime.datetime.now().time().strftime("%H:%M:%S")

	def __str__(self):
		return "[{}][{}][{}][{}]".format(
			self.name_of_class,
			self.subject[0],
			self.date,
			self.time
		)

def save_attendance_log(name_of_class, subject, attendance_list):
	attendance_log = AttendanceLog(name_of_class, subject, attendance_list)
	log_filename = attendance_log.__str__() + ".json"

	print(log_filename)

	json_string = json.dumps(attendance_log.__dict__)
	json_file = open(database_path + "/" + name_of_class + "/attendance_logs/" + log_filename, "w")
	json_file.write(json_string)

def view_logfile(filename):
	json_file = open(filename, "r")
	json_content = json_file.read()
	logfile = json.loads(json_content)

	print("Viewing attendance log:-")
	print("\tClass:".ljust(10), logfile["name_of_class"])
	subject = logfile["subject"]
	print("\tSubject:".ljust(10), subject[0].upper())
	print("\tTeacher:".ljust(10), subject[1].upper())
	print("\tDate:".ljust(10), logfile["date"])
	print("\tTime:".ljust(10), logfile["time"])
	print("\t\nAttendance List:-")

	i = 0
	for key in logfile["attendance_list"]:
		print(f"\t\t[{i}] {key.split('-')[1].upper()} ({key.split('-')[0]})".ljust(64), end = "")
		if logfile["attendance_list"][key]:
			print("Present")
		else:
			print("Absent")
		i += 1

	return logfile

if __name__ == '__main__':
	print("~ Welcome to the FaceRecAttTrackSys (FRATS) ~")
	while True:
		print("\nOptions: \n")
		print("1. Train Model")
		print("2. New Session")
		print("3. View Log")
		print("4. Quit")
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

				name_of_class = '-'.join(input("Class name? ").split()).upper()

				if not os.path.exists(database_path + "/" + name_of_class):
					os.mkdir(database_path + "/" + name_of_class)
					os.mkdir(database_path + "/" + name_of_class + "/student_images")
					os.mkdir(database_path + "/" + name_of_class + "/attendance_logs")
					os.mkdir(database_path + "/" + name_of_class + "/log_pdfs")
					number_of_students = int(input("Number of Students? "))
				else:
					print("Class already exists.")
					if input(("Do you want to add new students? (Y/N) ")).upper() == 'Y':
						number_of_students = int(input("Number of Students? "))
					else:
						continue
				
				print("Begin capturing...")

				for i in range(0, number_of_students):
					print("Student [{}]:".format(i + 1))
					registration_number = input("\tRegistration Number? ".ljust(25))
					name_of_student = input("\tStudent Name: ".ljust(25).format(i + 1)).upper()
					train_from_videostream(name_of_class, registration_number, name_of_student)

				build_subject_list(name_of_class)
				print("Database built for class {}.".format(name_of_class))

			elif choice == 2:
				print("2. Training from Pictures\n")
				print("Instructions:")
				print("\t1. Make a folder in the Database Path.")
				print("\t\tCurrent Database Path: " + database_path)
				print("\t2. Name the folder the name of the class.")
				print("\t3. Add the pictures of all the students of the class, labelled properly.")
		
		elif choice == 2:
			print("Starting new session...")

			# Display classes to choose from database
			print("Select class:-")
			for i in range(len(os.listdir(database_path))):
				print("[{}] {}".format(i, os.listdir(database_path)[i]))

			index = input("Index? ")
			try:
				index = int(index)
			except:
				print("Invalid index.")
				continue

			name_of_class = os.listdir(database_path)[index]

			# Fetch subject list from JSON File
			json_file = open(database_path + "/" + name_of_class + "/subject_list.json", "r")
			json_content = json_file.read()
			subject_list = json.loads(json_content)
			
			print("Select subject:-")
			for i in range(len(subject_list)):
				print("[{}] {}".format(i, subject_list[i]))

			while True:
				index = int(input("Index? "))
				if index in range(0, len(subject_list)):
					break

			subject = subject_list[index]
			print("Chosen subject: {}".format(subject[0]))

			# Take Attendance by going through student images
			student_list = os.listdir(database_path + "/" + name_of_class + "/student_images/")
			student_list.sort()

			attendance_list = {}

			for filename in student_list:
				print("DEBUG: {}".format(database_path + "/" + name_of_class + "/student_images/" + filename))
				img_reference = face_recognition.load_image_file(database_path + "/" + name_of_class + "/student_images/" + filename)
				img_reference = cv2.cvtColor(img_reference, cv2.COLOR_BGR2RGB)

				encode_reference = face_recognition.face_encodings(img_reference)[0]
				print(encode_reference)

				name_of_student = filename.split('.')[0].split('-')[1]
				registration_number = filename.split('.')[0].split('-')[0]

				print("Taking attedance for [{}] {}.".format(registration_number, name_of_student))
				attendance_list[registration_number + "-" + name_of_student] = recognize_face(encode_reference)

				print(attendance_list)

			# Save Attendance Log
			save_attendance_log(name_of_class, subject, attendance_list)

		elif choice == 3:
			print("Select class:-")
			for i in range(len(os.listdir(database_path))):
				print("\t[{}] {}".format(i, os.listdir(database_path)[i]))

			index = input("Index? ")
			try:
				index = int(index)
			except:
				print("Invalid index.")
				continue

			name_of_class = os.listdir(database_path)[index]

			# Get Attendance Logs

			attendance_path = os.listdir(database_path + "/" + name_of_class + "/attendance_logs")
			subjects = []

			# Show subjects
			print("Choose subject:-")
			for i in range(len(attendance_path)):
				if attendance_path[i].split('][')[1] not in subjects:
					subjects.append(attendance_path[i].split('][')[1])

			for i in range(len(subjects)):
				print(f"\t[{i}] {subjects[i]}")

			while True:
				subject_index = int(input("Index? "))
				if subject_index in range(len(attendance_path)):
					break

			# Show dates

			log_list = []

			print("Choose date and time:-")
			for log in attendance_path:
				if log.split('][')[1] == subjects[subject_index]:
					log_list.append(log)

			for i in range(len(log_list)):
				print("\t[{}] {} at {}".format(i, log_list[i].split('][')[2], log_list[i].split('][')[3]).split('.')[0][:-1])

			while True:
				index = int(input("Index? "))
				if index in range(len(log_list)):
					break

			log_object = view_logfile(database_path + "/" + name_of_class + "/attendance_logs/" + log_list[index])

			if input("Generate PDF? (Y/N) ").upper() == 'Y':
				pdf_filename = "'" + pdf_generator.generate_pdf(database_path, log_object) + "'"
				catch_error = os.system("xreader " + pdf_filename + " &")
				print("PDF generated and saved.")

				if input("Send log to {}? (Y/N) ".format(log_object["subject"][2])).upper() == 'Y':
					print("Sending...")
					log_sender.send_log(database_path, log_object)
					print("Email successfully sent.")

		elif choice == 4:
			print("Quitting...")
			quit()

		else:
			print("Invalid choice.")