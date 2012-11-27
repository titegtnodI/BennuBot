#Connect to the database
conn = sqlite3.connect(dbLoc)

#Patch stuff
setSetting("System", "version", {"Value":1}, conn)
mainWait = 0.01
setSetting("System", "mainWait", {"Value":mainWait}, conn)

#Load other settings normally
protoList = getSetting("System", "protoList", conn)[0][1].split(',')
plugList = getSetting("System", "plugList", conn)[0][1].split(',')
protoFolder = str(getSetting("System", "protoFolder", conn)[0][1])
plugFolder = str(getSetting("System", "plugFolder", conn)[0][1])
nick = str(getSetting("System", "nick", conn)[0][1])
quiet = str(getSetting("System", "quiet", conn)[0][1])
funcPrefix = str(getSetting("System", "funcPrefix", conn)[0][1])
protoPrefix = str(getSetting("System", "protoPrefix", conn)[0][1])
mainWait = float(getSetting("System", "mainWait", conn)[0][1])

#Close connection to the database
conn.close()
