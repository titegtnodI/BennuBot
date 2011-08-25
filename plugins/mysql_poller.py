import _mysql, time
plugName = 'MySQL Poller'
#TODO Array
#Channel[0], server[1], user[2], pass[3], db[4], table[5], index[6], [fields to output][7], currentpos[8]
mysqlPollerSetup = ['#channel', 'server', 'user', 'pass',
			'database', 'table', 'index', ['field1', 'field2', 'field3'], 0]
mysqlPollerFrequency = 60
mysqlPollerLast = 0

def load():
	global mysqlPollerSetup
	db = _mysql.connect(mysqlPollerSetup[1], mysqlPollerSetup[2], mysqlPollerSetup[3],
		mysqlPollerSetup[4])
	db.query('SELECT '+mysqlPollerSetup[6]+' FROM '+mysqlPollerSetup[5]+' ORDER BY '+
		mysqlPollerSetup[6]+' DESC LIMIT 1')
	mysqlPollerSetup[8] = int(db.use_result().fetch_row()[0][0])
	db.close()
	return mysqlPoller

def mysqlPoller(inMSG):
	global outMSG, mysqlPollerLast
	if time.time() - mysqlPollerFrequency >= mysqlPollerLast:
		db = _mysql.connect(mysqlPollerSetup[1], mysqlPollerSetup[2], mysqlPollerSetup[3],
			mysqlPollerSetup[4])
		db.query('SELECT '+mysqlPollerSetup[6]+' FROM '+mysqlPollerSetup[5]+' ORDER BY '+
				mysqlPollerSetup[6]+' DESC LIMIT 1')
		result = db.use_result().fetch_row()[0][0]
		if int(result) > mysqlPollerSetup[8]:
			outMSG += [['Table \"'+mysqlPollerSetup[5]+'\" updated: ', inMSG[1], inMSG[2],
					inMSG[3]]]
			for i in mysqlPollerSetup[7]:
				db.query('SELECT ' +i+' FROM '+mysqlPollerSetup[5]+' WHERE '+
					mysqlPollerSetup[6]+'='+str(mysqlPollerSetup[8]+1))
				outMSG += [['- Field \"'+i+'\": ' + db.use_result().fetch_row()[0][0],
						inMSG[1], inMSG[2], inMSG[3]]]
			mysqlPollerSetup[8] = int(result)
		db.close()
		mysqlPollerLast = time.time()
