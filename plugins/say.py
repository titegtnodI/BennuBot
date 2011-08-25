plugName = 'Say'

def say_say(inMSG):
	global outMSG
	outMSG += [[inMSG[0][len(inMSG[0].split()[0])+1:], inMSG[1], inMSG[2], inMSG[3]]]

def load():
	return {'say':say_say}
