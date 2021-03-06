from pdf_mail import sendpdf

def send_log(database_path, log_object):

	filename = "[{}][{}][{}][{}]".format(
		log_object["name_of_class"],
		log_object["subject"][0],
		log_object["date"],
		log_object["time"]
	)

	file_path = database_path + "/" + log_object["name_of_class"] + "/pdf_logs/"
	body = f'''
To {log_object["subject"][1]},
From Suraj Khati's FRATS Mini-Project :),\n
This message contains the attendance log for class {log_object["name_of_class"]}, for the date {log_object["date"]} at time {log_object["time"]}.

Please find attached the log PDF.

This message was auto generated by the program. You can
leave your suggestions in the reply.

Yours sincerely,
Suraj Khati's Program
'''

	k = sendpdf(
			"frats.project.smit@gmail.com",
			log_object["subject"][2],
			"fratsrocks@99",
			filename,
			body,
			filename,
			file_path
		)

	try:
		k.email_send()
	except:
		print("Some error occured trying to access the email account.")
		print("It might be caused due to Secure Access settings.")
		print("Please contact the administrator.")