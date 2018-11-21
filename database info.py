import csv
import sqlite3

# #Discrepancy (No Edits needed)
# with sqlite3.connect("discrepancy.db") as connection:
# 	c = connection.cursor()
# 	discrep = csv.reader(open(discrepancy, "rU"))
# 	c.execute("""CREATE TABLE discrepancy1(Discrepancy TEXT, Reservation TEXT, Event TEXT, Episode TEXT, DateOf TEXT, Start TEXT,
# 				Market TEXT, Zone TEXT, Network TEXT, ClientID INT, ClientName TEXT, ContractID TEXT, Rate TEXT, AE TEXT, Modified TEXT,
# 				ModifiedBy TEXT)""")
# 	c.executemany("""INSERT INTO discrepancy1(Discrepancy, Reservation, Event, Episode, DateOf, Start, Market, Zone, Network,
# 				ClientID, ClientName, ContractID, Rate, AE, Modified, ModifiedBy) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", discrep)	

# #AdCopyStatus (No Edits needed)
# with sqlite3.connect("AdCopyStatus.db") as connection:
# 	c = connection.cursor()
# 	adCopyStatus = csv.reader(open(arg1, "rU"))
# 	c.execute("""CREATE TABLE AdCopyStatus(ClientID INT, ClientName TEXT, AdCopyID INT, CutName TEXT, CutStart TEXT, Reason TEXT)""")
# 	c.executemany("""INSERT INTO AdCopyStatus(ClientID, ClientName, AdCopyID, CutName, CutStart, Reason) values (?, ?, ?, ?, ?, ?)""", adCopyStatus)

# #Copy Required (Edit Required)
# with sqlite3.connect("copyrequired.db") as connection:
# 	c = connection.cursor()
# 	copyRequired = arg1
# 	c.execute("""CREATE TABLE copyrequired(ClientID TEXT, ClientName TEXT, Rotation INT, RotDesc INT, SalesID INT, AE TEXT, SalOffID TEXT,
# 				SalOff TEXT, OrderNum INT, Networks TEXT, Regions TEXT, TotalRev TEXT, AvgPrty INT, DateNeed TEXT, Issue TEXT)""")
# 	c.executemany("""INSERT INTO copyrequired(ClientID, ClientName, Rotation, RotDesc, SalesID, AE, SalOffID, SalOff, OrderNum, Networks, 
# 				Regions, TotalRev, AvgPrty, DateNeed, Issue) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", copyRequired)

# #RSL (Edit Required)
# with sqlite3.connect("rsl.db") as connection:
# 	c = connection.cursor()
# 	rsl = arg1
# 	c.execute("""CREATE TABLE RSL(AE TEXT, Priority INT, ClientID INT, Client TEXT, ConID INT, LineNum INT, Zone TEXT, Network TEXT, DaysAuth TEXT,
# 				Mon INT, Tue INT, Wed INT, Thu INT, Fri INT, Sat INT, Sun INT, OldDates TEXT, Daypart TEXT, CGName TEXT, Total INT, Normal INT,
# 				Sched INT, Aired INT, ToDO INT, FinalWeek TEXT, Length INT, Program TEXT, Cost INT, LostRev INT, RD INT, NewDate TEXT, NewTime TEXT)""")
# 	c.executemany("""INSERT INTO RSL(AE, Priority, ClientID, Client, ConID, LineNum, Zone, Network, DaysAuth, Mon, Tue, Wed, Thu, Fri, Sat, Sun,
# 				OldDates, Daypart, CGName, Total, Normal, Sched, Aired, ToDO, FinalWeek, Length, Program, Cost, LostRev, RD, NewDate, NewTime)
# 				values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", rsl)

# #Unplaced (Edit Required)
# with sqlite3.connect("Unplaced.db") as connection:
# 	c = connection.cursor()
# 	unplaced = arg1
# 	c.execute("""CREATE TABLE unplacedSpots(OrderNum INT, OldDate TEXT, SpotName TEXT, Length INT, Description TEXT, Network TEXT, ClientID INT,
# 				Client TEXT, Phone TEXT, Initials TEXT, Rotation INT, Active TEXT, UCType TEXT, Retail INT, InvType TEXT, Billing TEXT, Market TEXT,
# 				Zone TEXT, Priority INT, Buy1 INT, BuyType TEXT, SpotsWeek INT, SpotsLine INT, MonAct TEXT, MonQua INT, TueAct TEXT, TueQua INT,
# 				WedAct TEXT, WedQua INT, ThuAct TEXT, ThuQua INT, FriAct TEXT, FriQua INT, SatAct TEXT, SatQua INT, SunAct TEXT, SunQua INT, Buy2 INT,
# 				Exception TEXT, Daypart TEXT, Entity TEXT, LineType TEXT, LineNum INT, OfficeID TEXT, Description2 TEXT, Name TEXT, OfficeName TEXT,
# 				Exception2 TEXT, Uniform TEXT, UniformReg TEXT, LineNum2 INT, Group INT, EndDate TEXT, Orbits TEXT, NewDate TEXT, NewTime TEXT)""")
# 	c.executemany("""INSERT INTO unplacedSpots(OrderNum, OldDate, SpotName, Length, Description, Network, ClientID, Client, Phone, Initials, Rotation,
# 				Active, UCType, Retail, InvType, Billing, Market, Zone, Priority, Buy1, BuyType, SpotsWeek, Spotsline, MonAct, MonQua, TueAct, TueQua,
# 				WedAct, WedQua, ThuAct, ThuQua, FriAct, FriQua, SatAct, SatQua, SunAct, SunQua, Buy2, Exception, Daypart, Entity, LineType, LineNum, OfficeID,
# 				Description2, Name, OfficeName, Exception2, Uniform, UniformReg, LineNum2, Group, EndDate, Orbits, NewDate, NewTime) values (?, ?, ?, ?,
# 				?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
# 				?, ?, ?, ?, ?, ?, ?, ?)""", unplaced)

def copyRequired_DiscrepDB(self, copy_req, discrep_rep):
	matches = [["Client Name", "Client ID", "ContractID", "Event", "Episode", "Date", "Time"]]
	for row in copy_req:
		for node in discrep_rep:
			if row[3] is in node[11]:
				matches.append([node[10], node[9], row[2], row[3], row[4], row[5]])
	return matches



