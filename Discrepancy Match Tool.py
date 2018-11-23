import csv
import sqlite3
from tkinter import *
from tkinter import filedialog, messagebox

"""Tool to compare two reports and provide specific information from matching lines"""

class MatchTool:
	UNPLACED_RSL_TEXT = [
		"Copy Required Report",
		"Ad Copy Status Report",
		"Unplaced Spots",
		"Required Spots",
		]

	def __init__(self, master):
		self.master = master
		master.geometry("400x300")
		master.title("Discrepancy Match Tool")

		self.top_frame = Frame(master)
		self.bottom_frame = Frame(master, width=400)

		self.csv_warning = Label(self.top_frame, text="All files must be csv files \nin order to work properly", relief=GROOVE)

		self.novar_button_var = IntVar()
		self.novar_button_var.set(0)
		self.novar_button = Checkbutton(self.top_frame, variable=self.novar_button_var, command=self.enableNovar)
		
		self.eclipse_button_var = IntVar()
		self.eclipse_button_var.set(0)
		self.eclipse_button = Checkbutton(self.top_frame, variable=self.eclipse_button_var, command=self.enableEclipse)

		self.missing_button_var = IntVar()
		self.missing_button_var.set(0)	
		self.missing_button = Checkbutton(self.top_frame, state=DISABLED, variable=self.missing_button_var, command=self.missingCopy)

		self.unplaced_button_var = IntVar()
		self.unplaced_button_var.set(0)
		self.unplaced_button = Checkbutton(self.top_frame, state=DISABLED, variable=self.unplaced_button_var, command=self.unplacedRSL)

		self.novar_label = Label(self.top_frame, text="Novar")
		self.eclipse_label = Label(self.top_frame, text="Eclipse/XG")
		self.missing_label = Label(self.top_frame, text="Missing Copy")

		self.unplaced_label_text = StringVar()
		self.unplaced_label_text.set("Unplaced or Required Spots")
		self.unplaced_label = Label(self.top_frame, textvariable=self.unplaced_label_text, width=22, anchor=constants.W)

		self.load_discrep = Button(self.bottom_frame, text="Load Discrepancy Report", width=25, command=self.loadDiscrep)
		self.load_discrep_file_name_text = StringVar()
		self.load_discrep_file_name = Label(self.bottom_frame, textvariable=self.load_discrep_file_name_text)

		self.submit = Button(self.bottom_frame, text="Submit", command=self.compareReports)

		self.load_unplaced_text = StringVar()
		self.load_unplaced_text.set("Load Report")
		self.load_unplaced = Button(self.bottom_frame, textvariable=self.load_unplaced_text, width=25, command=self.loadReports)

		self.load_unplaced_file_name_text = StringVar()
		self.load_unplaced_file_name = Label(self.bottom_frame, textvariable=self.load_unplaced_file_name_text)

		self.open_button = Button(self.bottom_frame, text="Save File", command=self.saveFile)
		self.help_button = Button(master, text="Help", command=self.help_instructions, width=6, height=1)
		

	#Layout
		self.top_frame.grid()
		self.bottom_frame.grid(row=1, pady=20)

		self.novar_button.grid()
		self.eclipse_button.grid(row=1)
		self.missing_button.grid(row=2)
		self.unplaced_button.grid(row=3)

		self.novar_label.grid(row=0, column=1, sticky=W)
		self.eclipse_label.grid(row=1, column=1, sticky=W)
		self.missing_label.grid(row=2, column=1, sticky=W)
		self.unplaced_label.grid(row=3, column=1, sticky=W)
		self.csv_warning.grid(row=1, rowspan=2, column=2, padx=10, ipadx=10, ipady=10)

		self.load_discrep.grid(row=0, pady=3, ipadx=5)
		self.load_discrep_file_name.grid(row=1, pady=3, ipadx=5)
		self.load_unplaced.grid(row=2, pady=3, ipadx=5)
		self.load_unplaced_file_name.grid(row=3, pady=3, ipadx=5)
		self.help_button.place(x=330, y=270)

	#Functions

	def enableNovar(self):
		"""Activates the Missing Copy and Unplaced Spots checkboxes, and disables the Novar checkbox"""
		if self.novar_button_var.get() == 1:
			self.eclipse_button["state"] = DISABLED
			self.missing_button["state"] = ACTIVE
			self.unplaced_button["state"] = ACTIVE
			self.unplaced_label_text.set(self.UNPLACED_RSL_TEXT[3])
		else:
			self.eclipse_button["state"] = ACTIVE
			self.missing_button["state"] = DISABLED
			self.unplaced_button["state"] = DISABLED
			self.unplaced_label_text.set("Unplaced or Required Spots")

	def enableEclipse(self):
		"""Activates the Missing Copy and Required Spots checkboxes, and disables the Eclipse checkbox"""
		if self.eclipse_button_var.get() == 1:
			self.novar_button["state"] = DISABLED
			self.missing_button["state"] = ACTIVE
			self.unplaced_button["state"] = ACTIVE
			self.unplaced_label_text.set(self.UNPLACED_RSL_TEXT[2])
		else:
			self.novar_button["state"] = ACTIVE
			self.missing_button["state"] = DISABLED
			self.unplaced_button["state"] = DISABLED
			self.unplaced_label_text.set("Unplaced or Required Spots")

	def missingCopy(self):
		"""Changes the value of missing_button_var to 1, changes text of unplaced_text, shows Submit button"""
		if self.missing_button_var.get() == 1:
			self.unplaced_button["state"] = DISABLED
			self.submit.grid(row=4, pady=5, ipadx=5)
			if self.novar_button_var.get() == 1:
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[1])
			elif self.eclipse_button_var.get() == 1:			
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[0])
		else:
			self.unplaced_button["state"] = ACTIVE
			self.load_unplaced_text.set("Load Report")
			self.submit.grid_forget()
			self.open_button.grid_forget()
			self.load_unplaced_file_name.grid_forget()

	def unplacedRSL(self):
		"""changes the value of unplaced_button_var to 1, changes text of unplaced_text, shows Submit button"""
		if self.unplaced_button_var.get() == 1:
			self.missing_button["state"] = DISABLED
			self.submit.grid(row=4, pady=5, ipadx=5)
			if self.novar_button_var.get() == 1:
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[3])
			elif self.eclipse_button_var.get() == 1:			
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[2])
		else:
			self.missing_button["state"] = ACTIVE
			self.load_unplaced_text.set("Load Report")
			self.submit.grid_forget()
			self.open_button.grid_forget()
			self.load_unplaced_file_name.grid_forget()

	def unplacedEdit(self, loaded_file):
		"""Opens the CSV file and edits the date and time for the Unplaced Spots report"""
		with open(loaded_file) as csv_file:
			unplaced_reader = csv.reader(csv_file, delimiter=',')
			unplaced_list = [row for row in unplaced_reader]
			unplaced_list.pop(0)
			unplaced_list[0].extend(['Date', 'Time'])
			for i in range(1, len(unplaced_list)):
				date_time = unplaced_list[i][1].split(' ')
				unplaced_list[i].append(date_time[0])
				time_of_day = int(date_time[1][:date_time[1].index(":")])
				if time_of_day < 13:
					date_time[1] = date_time[1] + " AM"
				else:
					time_of_day = time_of_day - 12
					date_time[1] = str(time_of_day) + date_time[1][date_time[1].index(":"):] + " PM"
				unplaced_list[i].append(date_time[1])
		return unplaced_list	

	def rslEdit(self, loaded_file):
		"""Edits the RSL report's Date and Time"""
		with open(loaded_file) as csv_file:
			rsl_reader = csv.reader(csv_file, delimiter=',')
			rsl_list = [row for row in rsl_reader]
			rsl_list[0].extend(['Date', 'Time'])
			for i in range(1, len(rsl_list)):
				date = rsl_list[i][16]
				date = date[:date.index("-")]
				new_date = date.split('/') #add 20 to the beginning of the year
				new_date[2] = "20" + new_date[2]
				date = new_date[0] + '/' + new_date[1] + '/' + new_date[2]
				month = int(date[:1])
				if month < 10:
					date = date[1:]
				time = rsl_list[i][17]
				time = time[:time.index("-")]
				rsl_list[i].append(date)
				rsl_list[i].append(time)
			for x in range(1, len(rsl_list)):
				digits = rsl_list[x][31]
				digits = int(digits[:digits.index(":")])
				if digits < 10:
					rsl_list[x][31] = rsl_list[x][31][1:] + " AM"
				elif digits < 13:
					rsl_list[x][31] = rsl_list[x][31] + " AM"
				else:
					digits = digits - 12
					rsl_list[x][31] = str(digits) + rsl_list[x][31][rsl_list[x][31].index(":"):] + " PM"
		return rsl_list

	def copyRequiredEdit(self, loaded_file):
		"""Removes the first row from the Copy Required Report"""
		with open(loaded_file) as csv_file:
			cr_reader = csv.reader(csv_file, delimiter=',')
			cr_list = [row for row in cr_reader]
			cr_list.pop(0)
		return cr_list

	def discrepEdit(self, loaded_file):
		"""Splits up the contract ID's into a list"""
		with open(loaded_file) as csv_file:
			discrep_reader = csv.reader(csv_file, delimiter=',')
			discrep_list = [row for row in discrep_reader]
			for i in range(1, len(discrep_list)):
				discrep_list[i][11] = discrep_list[i][11].split(';')
		return discrep_list

	def adCopyStatusEdit(self, loaded_file):
		"""Changes the AdCopyStatus report to a list"""
		with open(loaded_file) as csv_file:
			adCopy_reader = csv.reader(csv_file, delimiter=',')
			adCopy_list = [row for row in adCopy_reader]
			adCopy_list[0].append("ContractID")
			for i in range(1, len(adCopy_list)):
				conID = adCopy_list[i][6]
				conID = conID[conID.index(".") + 1:]
				adCopy_list[i].append(conID)
		return adCopy_list

	def copyRequired_DiscrepDB(self, copy_req, discrep_rep):
		"""Compares the Copy Required report to the Discrepancy Report to find matches"""
		matches = [["Client Name", "Client ID", "ContractID", "Event", "Episode", "Date", "Time"]]
		for row in copy_req:
			for node in discrep_rep:
				if row[3] in node[11]:
					matches.append([node[10], node[9], row[3], node[2], node[3], node[4], node[5]])
		return matches


	def unplacedSpots_DiscrepDB(self, copy_req, discrep_rep):
		matches = [["Discrepancy", "AE", "Client Name", "Client ID", "ContractID", "Line Number", "Zones","Network", "Date", "Time","Length"]]
		for i in range(1, len(copy_req)):
			match_count = 0
			for x in range(1, len(discrep_rep)):
				if copy_req[i][6] == discrep_rep[x][9]:
					if copy_req[i][0] in discrep_rep[x][11]:
						if copy_req[i][53] == discrep_rep[x][4]:
							if copy_req[i][54] == discrep_rep[x][5]:
								matches.append(["Yes", copy_req[i][45], copy_req[i][6], copy_req[i][7], copy_req[i][0], copy_req[i][42], copy_req[i][17], copy_req[i][5], copy_req[i][53], copy_req[i][54], copy_req[i][3]])
								match_count += 1
			if match_count == 0:
				matches.append(["No", copy_req[i][45], copy_req[i][6], copy_req[i][7], copy_req[i][0], copy_req[i][42], copy_req[i][17], copy_req[i][5], copy_req[i][53], copy_req[i][54], copy_req[i][3]])
		return matches

	def adCopy_DiscrepDB(self, copy_req, discrep_rep):
		matches = [["Client Name", "Client ID", "ContractID", "Event", "Episode", "Date", "Time"]]
		for row in copy_req:
			for node in discrep_rep:
				if row[7] in node[11]:
					matches.append([node[10], node[9], row[7], node[2], node[3], node[4], node[5]])
		return matches

	def rsl_DiscrepDB(self, copy_req, discrep_rep):
		match_count = 0
		matches = [["Discrepancy", "AE", "Client Name", "Client ID", "ContractID", "Line Number", "Zones","Network", "Date", "Time","Length"]]
		for i in range(1, len(copy_req)):
			match_count = 0
			for x in range(1, len(discrep_rep)):
				if copy_req[i][2] == discrep_rep[x][9]: #Client ID
					if copy_req[i][4] in discrep_rep[x][11]: #Contract
						if copy_req[i][6] == discrep_rep[x][7]: #Zone
							if copy_req[i][30] == discrep_rep[x][4]: #Date
								if copy_req[i][31] == discrep_rep[x][5]: #Time
									matches.append(["Yes", copy_req[i][0], copy_req[i][2], copy_req[i][3], copy_req[i][4], copy_req[i][5], copy_req[i][6], copy_req[i][7], copy_req[i][30], copy_req[i][31], copy_req[i][25]])
									match_count += 1
			if match_count == 0:
				matches.append(["No", copy_req[i][0], copy_req[i][2], copy_req[i][3], copy_req[i][4], copy_req[i][5], copy_req[i][6], copy_req[i][7], copy_req[i][30], copy_req[i][31], copy_req[i][25]])
		return matches			

	def loadDiscrep(self):
		"""Opens file directory for user to load report in xls format"""
		discrep_loaded = False
		discrepReport = filedialog.askopenfilename(
			filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
			)
		if not discrepReport:
			return
		else:
			self.load_discrep_file_name_text.set("Discrepancy Report loaded successfully")
			final_discrep = self.discrepEdit(discrepReport)
			discrep_loaded = True
			self.dis_loaded = discrep_loaded
			self.current_discrep = final_discrep
		return final_discrep, discrep_loaded

	def loadReports(self):
		"""Opens file directory for user to load file, file type depends on prior selections"""
		#Copy Required (Eclipse/Missing Copy)
		report_loaded = False
		if self.eclipse_button_var.get() == 1 and self.missing_button_var.get() == 1:
			copyRequired = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not copyRequired:
				return
			else:
				self.load_unplaced_file_name.grid(row=3, pady=3, ipadx=5)
				self.load_unplaced_file_name_text.set("Copy Required loaded successfully")
				final_report = self.copyRequiredEdit(copyRequired)
				report_loaded = True
				self.current_report = final_report
				self.loaded = report_loaded
				return final_report, report_loaded
		#AdCopyStatus (Novar/Missing Copy)
		elif self.novar_button_var.get() == 1 and self.missing_button_var.get() == 1:
			adCopyStatus = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not adCopyStatus:
				return
			else:
				self.load_unplaced_file_name.grid(row=3, pady=3, ipadx=5)
				self.load_unplaced_file_name_text.set("AdCopyStatus Report loaded successfully")
				final_report = self.adCopyStatusEdit(adCopyStatus)
				report_loaded = True
				self.current_report = final_report
				self.loaded = report_loaded
				return final_report, report_loaded
		#Unplaced Spots (Eclipse/Unplaced)
		elif self.eclipse_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			unplacedSpots = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not unplacedSpots:
				return
			else:
				self.load_unplaced_file_name.grid(row=3, pady=3, ipadx=5)
				self.load_unplaced_file_name_text.set("Unplaced Spots Report loaded successfully")
				final_report = self.unplacedEdit(unplacedSpots)
				report_loaded = True
				self.current_report = final_report
				self.loaded = report_loaded
				return final_report, report_loaded
		#RSL (Novar/Unplaced)
		elif self.novar_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			requiredSpots = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not requiredSpots:
				return
			else:
				self.load_unplaced_file_name.grid(row=3, pady=3, ipadx=5)
				self.load_unplaced_file_name_text.set("Required Spots loaded successfully")
				final_report = self.rslEdit(requiredSpots)
				report_loaded = True
				self.current_report = final_report
				self.loaded = report_loaded
				return final_report, report_loaded

	def compareReports(self):
		"""Compares two loaded reports"""
		#CopyRequired (Eclipse/Missing Copy)
		self.open_button.grid(row=5, pady=5, ipadx=5)
		if self.eclipse_button_var.get() == 1 and self.missing_button_var.get() == 1:
			try:
				matches = self.copyRequired_DiscrepDB(self.current_report, self.current_discrep)
			except AttributeError:
				messagebox.showerror("Error", "Please enter both required reports")
			else:
				self.output_report = matches
				return matches
		#AdCopyStatus (Novar/Missing Copy)
		elif self.novar_button_var.get() == 1 and self.missing_button_var.get() == 1:
			try:
				matches = self.adCopy_DiscrepDB(self.current_report, self.current_discrep)
			except AttributeError:
				messagebox.showerror("Error", "Please enter both required reports")
			else:
				self.output_report = matches
				return matches
		#Unplaced Spots (Eclipse/Unplaced)
		elif self.eclipse_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			try:
				matches = self.unplacedSpots_DiscrepDB(self.current_report, self.current_discrep)
			except AttributeError:
				messagebox.showerror("Error", "Please enter both required reports")
			else:
				self.output_report = matches
				return matches
		#RSL (Novar/Unplaced)
		elif self.novar_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			try:
				matches = self.rsl_DiscrepDB(self.current_report, self.current_discrep)
			except AttributeError:
				messagebox.showerror("Error", "Please enter both required reports")
			else:
				self.output_report = matches
				return matches

	def saveFile(self):
		"""Saves the data as a csv file"""
		filepath = filedialog.asksaveasfilename(
			defaultextension=".csv",
			filetypes=[("CSV File", "*.csv")],)
		if not filepath:
			return
		else:
			with open(filepath, "w", newline='') as output_file:
				writer = csv.writer(output_file)
				writer.writerows(self.output_report)

	def help_instructions(self):
		"""Provides instructions on how to use the tool"""
		messagebox.showinfo("Help", """Save all reports as .csv files 
							\nSelect If you are in a Novar or Eclipse/XG market
							 \nSelect one of the report types 
							 \nLoad the Discrepancy report and your specified report in 
							 \nClick on Submit, this will compare the two reports
							 \nClick on Save, this will give you option to save the output report
							 \nYou can now clear out your submissions and enter a new one if you please""")

# Format the tool better
	#Remove checks if button gets disabled
root = Tk()
interface = MatchTool(root)
root.mainloop()
