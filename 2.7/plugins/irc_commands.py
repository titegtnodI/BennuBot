#IRC only (Protocol 'irc')
#TODO /invite <nick>
plugName = 'IRC Commands'

def irc_set(inMSG, mode):
	level = getPermission(inMSG)
	if (inMSG[1] != 'irc' or (mode[1] == 'v' and level < 1) or (mode[1] == 'h' and level < 2) or
		(mode[1] == 'o' and level < 3) or (mode[1] == 'a' and level < 6)): return
	arrayMSG = inMSG[0].split(None, 3)
	if len(arrayMSG) == 1:
		IRCsocks[inMSG[2]].send('mode ' + inMSG[3] + ' ' + mode + ' ' + inMSG[4] + '\r\n')
	elif len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('mode ' + inMSG[3] + ' ' + mode + ' ' + arrayMSG[1] + '\r\n')
	elif len(arrayMSG) == 3:
		IRCsocks[inMSG[2]].send('mode ' + arrayMSG[2] + ' ' + mode + ' ' + arrayMSG[1] + '\r\n')

#TODO Allow for channel to be specified.
def irc_kick(inMSG):
	if inMSG[1] != 'irc' or getPermission(inMSG) < 4: return
	arrayMSG = inMSG[0].split(None, 2)
	if len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('kick ' + inMSG[3] + ' ' + arrayMSG[1] + '\r\n')
	elif len(arrayMSG) > 2:
		IRCsocks[inMSG[2]].send('kick ' + inMSG[3] + ' ' + arrayMSG[1] + ' :' + arrayMSG[2] + '\r\n')

def irc_kickban(inMSG, plusOrMinus='+'):
	if inMSG[1] != 'irc' or getPermission(inMSG) < 5: return
	arrayMSG = inMSG[0].split(None, 3)
	if 'kb' in arrayMSG[0]: irc_kick(inMSG)
	if len(arrayMSG) > 2 and ('kb' in command or 'bk' in command):
		IRCsocks[inMSG[2]].send('mode ' + inMSG[3] + ' ' + plusOrMinus + 'b ' + arrayMSG[2] + '\r\n')
	else:
		IRCsocks[inMSG[2]].send('mode ' + inMSG[3] + ' ' + plusOrMinus + 'b ' + arrayMSG[1] + '\r\n')
	if 'bk' in arrayMSG[0]: irc_kick(inMSG)
	

def irc_action(inMSG):
    if inMSG[1] == 'irc':
        return '\x01ACTION ' + inMSG[0].split(None, 1)[1] + '\x01'

def load():
	return {'op':(lambda x:irc_set(x, '+o')), 'deop':(lambda x:irc_set(x, '-o')),
		'hop':(lambda x:irc_set(x, '+h')), 'dehop':(lambda x:irc_set(x, '-h')),
		'kick':irc_kick, 'ban':irc_kickban, 'unban':(lambda x:irc_kickban(x, '-')), 'kb':irc_kickban,
		'bk':irc_kickban, 'voice':(lambda x:irc_set(x, '+v')), 'devoice':(lambda x:irc_set(x, '-v')),
		'admin':(lambda x:irc_set(x, '+a')), 'deadmin':(lambda x:irc_set(x, '-a')),
		'do':irc_action, 'mod':(lambda x:irc_set(x, '+m')), 'demod':(lambda x:irc_set(x, '-m'))}
