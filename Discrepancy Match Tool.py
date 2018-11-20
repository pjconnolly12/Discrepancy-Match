import csv
import sqlite3
from tkinter import *
from tkinter import filedialog

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
		master.geometry("250x200")
		master.title("Discrepancy Match Tool")

		self.novar_button_var = IntVar()
		self.novar_button_var.set(0)
		self.novar_button = Checkbutton(master, variable=self.novar_button_var, command=self.enableNovar)
		
		self.eclipse_button_var = IntVar()
		self.eclipse_button_var.set(0)
		self.eclipse_button = Checkbutton(master, variable=self.eclipse_button_var, command=self.enableEclipse)

		self.missing_button_var = IntVar()
		self.missing_button_var.set(0)	
		self.missing_button = Checkbutton(master, state=DISABLED, variable=self.missing_button_var, command=self.missingCopy)

		self.unplaced_button_var = IntVar()
		self.unplaced_button_var.set(0)
		self.unplaced_button = Checkbutton(master, state=DISABLED, variable=self.unplaced_button_var, command=self.unplacedRSL)

		self.novar_label = Label(master, text="Novar")
		self.eclipse_label = Label(master, text="Eclipse/XG")
		self.missing_label = Label(master, text="Missing Copy")

		self.unplaced_label_text = StringVar()
		self.unplaced_label_text.set("Unplaced or Required Spots")
		self.unplaced_label = Label(master, textvariable=self.unplaced_label_text, width=22, anchor=constants.W)

		self.load_discrep = Button(master, text="Load Discrepancy Report", width=25, command=self.loadDiscrep)
		self.submit = Button(master, text="Submit")

		self.load_unplaced_text = StringVar()
		self.load_unplaced_text.set("Load Report")
		self.load_unplaced = Button(master, textvariable=self.load_unplaced_text, width=25, command=self.loadReports)

	#Layout

		self.novar_button.grid()
		self.eclipse_button.grid(row=1)
		self.missing_button.grid(row=2)
		self.unplaced_button.grid(row=3)

		self.novar_label.grid(row=0, column=1, sticky=W)
		self.eclipse_label.grid(row=1, column=1, sticky=W)
		self.missing_label.grid(row=2, column=1, sticky=W)
		self.unplaced_label.grid(row=3, column=1, sticky=W)

		self.load_discrep.grid(row=4, columnspan=2, sticky=W, pady=3, ipadx=5)
		self.load_unplaced.grid(row=5, columnspan=2, sticky=W, pady=3, ipadx=5)

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
			self.submit.grid(row=6, columnspan=2, pady=5)
			if self.novar_button_var.get() == 1:
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[1])
			elif self.eclipse_button_var.get() == 1:			
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[0])
		else:
			self.unplaced_button["state"] = ACTIVE
			self.load_unplaced_text.set("Load Report")
			self.submit.grid_forget()

	def unplacedRSL(self):
		"""changes the value of unplaced_button_var to 1, changes text of unplaced_text, shows Submit button"""
		if self.unplaced_button_var.get() == 1:
			self.missing_button["state"] = DISABLED
			self.submit.grid(row=6, columnspan=2, pady=5)
			if self.novar_button_var.get() == 1:
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[3])
			elif self.eclipse_button_var.get() == 1:			
				self.load_unplaced_text.set("Load " + self.UNPLACED_RSL_TEXT[2])
		else:
			self.missing_button["state"] = ACTIVE
			self.load_unplaced_text.set("Load Report")
			self.submit.grid_forget()

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

	def discrepancyDB(self, discrepancy):
		"""creates SQL database from the discrepancy report"""
		with sqlite3.connect("DiscrepMatch.db") as connection:
			c = connection.cursor()
			discrep = csv.reader(open(discrepancy, "rU"))
			c.execute("""CREATE TABLE discrepancy1(Discrepancy TEXT, Reservation TEXT, Event TEXT, Episode TEXT, DateOf TEXT, Start TEXT,
				Market TEXT, Zone TEXT, Network TEXT, ClientID INT, ClientName TEXT, ContractID TEXT, Rate TEXT, AE TEXT, Modified TEXT,
				ModifiedBy TEXT)""")
			c.executemany("""INSERT INTO discrepancy1(Discrepancy, Reservation, Event, Episode, DateOf, Start, Market, Zone, Network,
				ClientID, ClientName, ContractID, Rate, AE, Modified, ModifiedBy) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", discrep)

	#AdCopyStatus (No Edits needed)
	def adCopyDB(self, ad_copy):
		"""creates SQL database from the ad copy status report"""
		with sqlite3.connect("DiscrepMatch.db") as connection:
			c = connection.cursor()
			adCopyStatus = csv.reader(open(ad_copy, "rU"))
			c.execute("""CREATE TABLE AdCopyStatus(ClientID INT, ClientName TEXT, AdCopyID INT, CutName TEXT, CutStart TEXT, CutStop TEXT, Reason TEXT)""")
			c.executemany("""INSERT INTO AdCopyStatus(ClientID, ClientName, AdCopyID, CutName, CutStart, CutStop, Reason) values (?, ?, ?, ?, ?, ?, ?)""", adCopyStatus)

#Copy Required (Edit Required)
	def copyRequiredDB(self, copy_required):
		"""creates SQL database from the copy required report"""
		with sqlite3.connect("DiscrepMatch.db") as connection:
			c = connection.cursor()
			copyRequired = copy_required
			c.execute("""CREATE TABLE copyrequired(ClientID TEXT, ClientName TEXT, Rotation INT, RotDesc INT, SalesID INT, AE TEXT, SalOffID TEXT,
				SalOff TEXT, OrderNum INT, Networks TEXT, Regions TEXT, TotalRev TEXT, AvgPrty INT, DateNeed TEXT, Issue TEXT)""")
			c.executemany("""INSERT INTO copyrequired(ClientID, ClientName, Rotation, RotDesc, SalesID, AE, SalOffID, SalOff, OrderNum, Networks, 
				Regions, TotalRev, AvgPrty, DateNeed, Issue) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", copyRequired)

#RSL (Edit Required)
	def rslDB(self, rsl_report):
		"""creates SQL database from the RSL report"""
		with sqlite3.connect("DiscrepMatch.db") as connection:
			c = connection.cursor()
			rsl = rsl_report
			c.execute("""CREATE TABLE RSL(AE TEXT, Priority INT, ClientID INT, Client TEXT, ConID INT, LineNum INT, Zone TEXT, Network TEXT, DaysAuth TEXT,
				Mon INT, Tue INT, Wed INT, Thu INT, Fri INT, Sat INT, Sun INT, OldDates TEXT, Daypart TEXT, CGName TEXT, Total INT, Normal INT,
				Sched INT, Aired INT, ToDO INT, FinalWeek TEXT, Length INT, Program TEXT, Cost INT, LostRev INT, RD INT, NewDate TEXT, NewTime TEXT)""")
			c.executemany("""INSERT INTO RSL(AE, Priority, ClientID, Client, ConID, LineNum, Zone, Network, DaysAuth, Mon, Tue, Wed, Thu, Fri, Sat, Sun,
				OldDates, Daypart, CGName, Total, Normal, Sched, Aired, ToDO, FinalWeek, Length, Program, Cost, LostRev, RD, NewDate, NewTime)
				values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", rsl)

#Unplaced (Edit Required)
	def unplacedDB(self, unplaced_report):
		"""Creates SQL database from the unplaced spot report"""
		with sqlite3.connect("DiscrepMatch.db") as connection:
			c = connection.cursor()
			unplaced = unplaced_report
			c.execute("""CREATE TABLE unplacedSpots(OrderNum INT, OldDate TEXT, SpotName TEXT, Length INT, Description TEXT, Network TEXT, ClientID INT,
					Client TEXT, Phone TEXT, Initials TEXT, Rotation INT, Active TEXT, UCType TEXT, Retail INT, InvType TEXT, Billing TEXT, Market TEXT,
					Zone TEXT, Priority INT, Buy1 INT, BuyType TEXT, SpotsWeek INT, SpotsLine INT, MonAct TEXT, MonQua INT, TueAct TEXT, TueQua INT,
					WedAct TEXT, WedQua INT, ThuAct TEXT, ThuQua INT, FriAct TEXT, FriQua INT, SatAct TEXT, SatQua INT, SunAct TEXT, SunQua INT, Buy2 INT,
					Exception TEXT, Daypart TEXT, Entity TEXT, LineType TEXT, LineNum INT, OfficeID TEXT, Description2 TEXT, Name TEXT, OfficeName TEXT,
					Exception2 TEXT, Uniform TEXT, LineNum2 INT, "Group" INT, EndDate TEXT, Orbits TEXT, NewDate TEXT, NewTime TEXT)""")
			c.executemany("""INSERT INTO unplacedSpots(OrderNum, OldDate, SpotName, Length, Description, Network, ClientID, Client, Phone, Initials, Rotation,
					Active, UCType, Retail, InvType, Billing, Market, Zone, Priority, Buy1, BuyType, SpotsWeek, Spotsline, MonAct, MonQua, TueAct, TueQua,
					WedAct, WedQua, ThuAct, ThuQua, FriAct, FriQua, SatAct, SatQua, SunAct, SunQua, Buy2, Exception, Daypart, Entity, LineType, LineNum, OfficeID,
					Description2, Name, OfficeName, Exception2, Uniform, LineNum2, "Group", EndDate, Orbits, NewDate, NewTime) values (?, ?, ?, ?,
					?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
					?, ?, ?, ?, ?, ?, ?, ?)""", unplaced)

	def loadDiscrep(self):
		"""Opens file directory for user to load report in xls format"""
		discrepReport = filedialog.askopenfilename(
			filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
			)
		if not discrepReport:
			return
		else:
			self.discrepancyDB(discrepReport)

	def loadReports(self):
		"""Opens file directory for user to load file, file type depends on prior selections"""
		#Copy Required (Eclipse/Missing Copy)
		if self.eclipse_button_var.get() == 1 and self.missing_button_var.get() == 1:
			copyRequired = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not copyRequired:
				return
			else:
				copyRequired = self.copyRequiredEdit(copyRequired)
				self.copyRequiredDB(copyRequired)
		#AdCopyStatus (Novar/Missing Copy)
		elif self.novar_button_var.get() == 1 and self.missing_button_var.get() == 1:
			adCopyStatus = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not adCopyStatus:
				return
			else:
				self.adCopyDB(adCopyStatus)	
		#Unplaced Spots (Eclipse/Unplaced)
		elif self.eclipse_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			unplacedSpots = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not unplacedSpots:
				return
			else:
				unplacedSpots = self.unplacedEdit(unplacedSpots)
				self.unplacedDB(unplacedSpots)
		#RSL (Novar/Unplaced)
		elif self.novar_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			requiredSpots = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not requiredSpots:
				return
			else:
				requiredSpots = self.rslEdit(requiredSpots)
				self.rslDB(requiredSpots)

# Add functionality for the Submit button: finds the matches between the two db's opened up and returns them as CSV
	# Should I use :memory: or actual db's?
		# Will :memory: work once the function is over? Won't it close the db being used?
	# How can I write back to a CSV?	
# Add fields under Load buttons to show the file name that was loaded
# Format the tool better

root = Tk()
interface = MatchTool(root)
root.mainloop()


