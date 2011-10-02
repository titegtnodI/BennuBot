#IRC only (Protocol 'irc')
#TODO Integrate with permission system (When it's in place)
plugName = 'IRC Commands'

def irc_unavailable(inMSG):
	if inMSG[1] != 'irc' or not isAdmin(inMSG): return
	if not quiet:
		sendMSG('Sorry, that command is not yet available.', inMSG[1], inMSG[2], inMSG[3])

def irc_set(inMSG, mode):
	if inMSG[1] != 'irc' or not isAdmin(inMSG): return
	arrayMSG = inMSG[0].split()
	if len(arrayMSG) == 1:
		IRCsocks[inMSG[2]].send('mode ' + inMSG[3] + ' ' + mode + ' ' + inMSG[4] + '\r\n')
	elif len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('mode ' + inMSG[3] + ' ' + mode + ' ' + arrayMSG[1] + '\r\n')
	elif len(arrayMSG) == 3:
		IRCsocks[inMSG[2]].send('mode ' + arrayMSG[2] + ' ' + mode + ' ' + arrayMSG[1] + '\r\n')

def irc_action(inMSG):
	if inMSG[1] != 'irc': return
	sendMSG('\x01ACTION ' + inMSG[0].split(None, 1)[1] + '\x01', inMSG[1], inMSG[2], inMSG[3])

def load():
	return {'op':(lambda x:irc_set(x, '+o')), 'deop':(lambda x:irc_set(x, '-o')),
		'hop':(lambda x:irc_set(x, '+h')), 'dehop':(lambda x:irc_set(x, '-h')),
		'kick':irc_unavailable, 'ban':irc_unavailable, 'kb':irc_unavailable,
		'voice':(lambda x:irc_set(x, '+v')), 'devoice':(lambda x:irc_set(x, '-v')),
		'admin':(lambda x:irc_set(x, '+a')), 'deadmin':(lambda x:irc_set(x, '-a')),
		'do':irc_action}
