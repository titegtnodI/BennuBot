plugName = 'Local Python Exec'

def load():
	return {'pyexec':localPythonExec}

def localPythonExec(inMSG):
	global outMSG
	if not isAdmin(inMSG):
		outMSG.append(['Not authorized.', inMSG[1], inMSG[2], inMSG[3]])
		return
	try:
		exec inMSG[0].split(None, 1)[1]
		outMSG.append(['Done.', inMSG[1], inMSG[2], inMSG[3]])
	except Exception as e:
		outMSG.append([str(e), inMSG[1], inMSG[2], inMSG[3]])
