plugName = 'Say'

def say_say(inMSG):
	global outMSG
	outMSG.append([inMSG[0].split(None, 1)[1], inMSG[1], inMSG[2], inMSG[3]])

def load():
	return {'say':say_say}
