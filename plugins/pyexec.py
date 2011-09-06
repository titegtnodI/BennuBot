plugName = 'Local Python Exec'

def load():
	return {'pyexec':localPythonExec}

def localPythonExec(inMSG):
	global outMSG
	if not isAdmin(inMSG):
		outMSG += [['Not authorized.', inMSG[1], inMSG[2], inMSG[3]]]
		return
	try:
		exec inMSG[0][inMSG[0].index(' ')+1:]
		outMSG += [['Done.', inMSG[1], inMSG[2], inMSG[3]]]
	except Exception as e:
		outMSG += [[str(e), inMSG[1], inMSG[2], inMSG[3]]]
