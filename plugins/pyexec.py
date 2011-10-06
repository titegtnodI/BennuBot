plugName = 'Local Python Exec'

def load():
	return {'pyexec':localPythonExec}

def localPythonExec(inMSG):
	if getPermission(inMSG) < 1000:
		outMSG.append(['Not authorized.', inMSG[1], inMSG[2], inMSG[3]])
		return
	try:
		exec inMSG[0].split(None, 1)[1]
		sendMSG('Done.', inMSG[1], inMSG[2], inMSG[3])
	except Exception as e:
		sendMSG(str(e), inMSG[1], inMSG[2], inMSG[3])
