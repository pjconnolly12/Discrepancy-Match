import csv
import sqllite3

#Discrepancy (No Edits needed)
with sqllite3.connect("discrepancy.db") as connection:
	c = connection.cursor()
	discrep = csv.reader(open(discrepancy, "rU"))
	c.execute("""CREATE TABLE discrepancy1(Discrepancy TEXT, Reservation TEXT, Event TEXT, Episode TEXT, DateOf TEXT, Start TEXT,
				Market TEXT, Zone TEXT, Network TEXT, ClientID INT, ClientName TEXT, ContractID TEXT, Rate TEXT, AE TEXT, Modified TEXT,
				ModifiedBy TEXT)""")
	c.executemany("""INSERT INTO discrepancy1(Discrepancy, Reservation, Event, Episode, DateOf, Start, Market, Zone, Network,
				ClientID, ClientName, ContractID, Rate, AE, Modified, ModifiedBy) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", discrep)	

#AdCopyStatus (No Edits needed)
with sqllite3.connect("AdCopyStatus.db") as connection:
	c = connection.cursor()
	adCopyStatus = csv.reader(open(arg1, "rU"))
	c.execute("""CREATE TABLE AdCopyStatus(ClientID INT, ClientName TEXT, AdCopyID INT, CutName TEXT, CutStart TEXT, Reason TEXT)""")
	c.executemany("""INSERT INTO AdCopyStatus(ClientID, ClientName, AdCopyID, CutName, CutStart, Reason) values (?, ?, ?, ?, ?, ?)""", adCopyStatus)

#Copy Required (Edit Required)
with sqllite3.connect("copyrequired.db") as connection:
	c = connection.cursor()
	copyRequired = arg1
	c.execute("""CREATE TABLE copyrequired(ClientID TEXT, ClientName TEXT, Rotation INT, RotDesc INT, SalesID INT, AE TEXT, SalOffID TEXT,
				SalOff TEXT, OrderNum INT, Networks TEXT, Regions TEXT, TotalRev TEXT, AvgPrty INT, DateNeed TEXT, Issue TEXT)""")
	c.executemany("""INSERT INTO copyrequired(ClientID, ClientName, Rotation, RotDesc, SalesID, AE, SalOffID, SalOff, OrderNum, Networks, 
				Regions, TotalRev, AvgPrty, DateNeed, Issue) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", copyRequired)

