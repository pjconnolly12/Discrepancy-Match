import csv
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


	def loadDiscrep(self):
		"""Opens file directory for user to load report in xls format"""
		discrepReport = filedialog.askopenfilename(
			filetypes=[("Excel File", "*.xls"), ("All Files", "*.*")]
			)
		if not discrepReport:
			return

	def loadReports(self):
		"""Opens file directory for user to load file, file type depends on prior selections"""
		#Copy Required (Eclipse/Missing Copy)
		if self.eclipse_button_var.get() == 1 and self.missing_button_var.get() == 1:
			copyRequired = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not copyRequired:
				return
		#AdCopyStatus (Novar/Missing Copy)
		elif self.novar_button_var.get() == 1 and self.missing_button_var.get() == 1:
			adCopyStatus = filedialog.askopenfilename(
				filetypes=[("XML File", "*.xml"), ("All Files", "*.*")]
				)
			if not adCopyStatus:
				return	
		#Unplaced Spots (Eclipse/Unplaced)
		elif self.eclipse_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			unplacedSpots = filedialog.askopenfilename(
				filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
				)
			if not unplacedSpots:
				return
		#RSL (Novar/Unplaced)
		elif self.novar_button_var.get() == 1 and self.unplaced_button_var.get() == 1:
			requiredSpots = filedialog.askopenfilename(
				filetypes=[("XML File", "*.xml"), ("All Files", "*.*")]
				)
			if not requiredSpots:
				return


root = Tk()
interface = MatchTool(root)
root.mainloop()


