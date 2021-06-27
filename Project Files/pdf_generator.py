from fpdf import FPDF

def generate_pdf(database_path, log_object):
	pdf = FPDF(format = 'letter', unit = 'in')
	pdf.add_page()
	pdf.set_font('Times', '', 10.0) 
	epw = pdf.w - 2 * pdf.l_margin

	col_width = epw / 3

	data = [
		['RegNo', 'Name', 'Absent/Present'],
	]

	number_present = 0
	for key in log_object["attendance_list"]:
		registration_number = key.split('-')[0]
		name_of_student = key.split('-')[1]
		if log_object["attendance_list"][key]:
			presence = "Present"
			number_present += 1
		else:
			presence = "Absent"

		data.append([registration_number, name_of_student, presence])

	th = pdf.font_size
	pdf.set_font('Times','B',14.0)
	pdf.cell(epw, 0.0, 'Attendance Log', align='C')
	pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Class"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, log_object["name_of_class"], border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Subject"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, log_object["subject"][0].upper(), border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Teacher"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, log_object["subject"][1].upper(), border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Teacher's Email"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, log_object["subject"][2], border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Date"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, log_object["date"], border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Time"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, log_object["time"], border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Total Students"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, str(len(log_object["attendance_list"])), border = 1); pdf.ln(2 * th)
	pdf.set_font('Times', 'B', 10.0); pdf.cell(epw/7, 2 * th, str("Present"), border = 1); pdf.set_font(''); pdf.cell(epw - epw/7, 2 * th, str(number_present), border = 1); pdf.ln(2 * th)

	pdf.ln(2 * th)

	pdf.set_font('Times', 'B', 10)
	pdf.set_fill_color(225, 230, 181)

	# Title
	pdf.cell(epw / 7, 2 * th, str(data[0][0]), border = 1, fill = True)
	pdf.cell((epw - (epw / 7)) / 2, 2 * th, str(data[0][1]), border = 1, fill = True)
	pdf.cell((epw - (epw / 7)) / 2, 2 * th, str(data[0][2]), border = 1, fill = True)

	pdf.ln(2 * th)
	data.pop(0)

	# Remove Bold
	pdf.set_font('')

	cell_colors = [
		(196, 145, 100),
		(200, 200, 200)
	]

	# Here we add more padding by passing 2*th as height
	for i in range(len(data)):
		color = cell_colors[i % 2]
		pdf.set_fill_color(color[0], color[1], color[2])

		pdf.cell(epw / 7, 2 * th, str(data[i][0]), border = 1, fill = True)
		pdf.cell((epw - (epw / 7)) / 2, 2 * th, str(data[i][1]).upper(), border = 1, fill = True)
		if data[i][2].upper() == 'PRESENT':
			pdf.set_fill_color(0, 255, 0)
		else:
			pdf.set_fill_color(255, 0, 0)
		pdf.cell((epw - (epw / 7)) / 2, 2 * th, str(data[i][2]).upper(), border = 1, fill = True)

		# for datum in data[i]:
			# Enter data in colums
			# pdf.cell(col_width, 2 * th, str(datum), border = 1, fill = True)
	 
		pdf.ln(2 * th)
	
	pdf_filename = "[{}][{}][{}][{}].pdf".format(
		log_object["name_of_class"],
		log_object["subject"][0],
		log_object["date"],
		log_object["time"]
	)

	pdf.output(database_path + "/" + log_object["name_of_class"] + "/pdf_logs/" + pdf_filename, 'F')
	return database_path + "/" + log_object["name_of_class"] + "/pdf_logs/" + pdf_filename