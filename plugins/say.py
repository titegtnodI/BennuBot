plugName = 'Say'

def say_say(inMSG):
	global outMSG
	outMSG += [[inMSG[0][4:], inMSG[1], inMSG[2], inMSG[3]]]

def load():
	return {'say':say_say}
