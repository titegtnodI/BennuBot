plugName = 'Say'

def say_say(inMSG):
	msg = inMSG[0].split(None, 1)
	if len(msg) > 1:
		sendMSG(msg[1], inMSG[1], inMSG[2], inMSG[3])

def say_reverse(inMSG):
	msg = inMSG[0].split(None, 1)
	if len(msg) > 1:
		sendMSG(msg[1][::-1], inMSG[1], inMSG[2], inMSG[3])

def load():
	return {'say':say_say, 'rev':say_reverse}
