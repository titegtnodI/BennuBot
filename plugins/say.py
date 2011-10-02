plugName = 'Say'

def say_say(inMSG):
	sendMSG(inMSG[0].split(None, 1)[1], inMSG[1], inMSG[2], inMSG[3])

def say_reverse(inMSG):
	sendMSG(inMSG[0].split(None, 1)[1][::-1], inMSG[1], inMSG[2], inMSG[3])

def load():
	return {'say':say_say, 'rev':say_reverse}
