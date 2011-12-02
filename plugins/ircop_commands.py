#IRC only (Protocol 'irc')
plugName = 'IRCOP Commands'

def irc_oset(inMSG, mode):
	level = getPermission(inMSG)
	if (inMSG[1] != 'irc' or (mode[1] == 'v' and level < 501) or (mode[1] == 'h' and level < 502) or
		(mode[1] == 'o' and level < 503) or (mode[1] == 'a' and level < 506)): return
	arrayMSG = inMSG[0].split(None, 3)
	if len(arrayMSG) == 1:
		IRCsocks[inMSG[2]].send('omode ' + inMSG[3] + ' ' + mode + ' ' + inMSG[4] + '\r\n')
	elif len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('omode ' + inMSG[3] + ' ' + mode + ' ' + arrayMSG[1] + '\r\n')
	elif len(arrayMSG) == 3:
		IRCsocks[inMSG[2]].send('omode ' + arrayMSG[2] + ' ' + mode + ' ' + arrayMSG[1] + '\r\n')

#TODO Allow for channel to be specified.
def irc_okick(inMSG):
	if inMSG[1] != 'irc' or getPermission(inMSG) < 504: return
	arrayMSG = inMSG[0].split(None, 2)
	if len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('okick ' + inMSG[3] + ' ' + arrayMSG[1] + '\r\n')
	elif len(arrayMSG) > 2:
		IRCsocks[inMSG[2]].send('okick ' + inMSG[3] + ' ' + arrayMSG[1] + ' :' + arrayMSG[2] + '\r\n')

def irc_okickban(inMSG, plusOrMinus='+'):
	if inMSG[1] != 'irc' or getPermission(inMSG) < 505: return
	arrayMSG = inMSG[0].split(None, 3)
	if 'okb' in arrayMSG[0]: irc_kick(inMSG)
	if len(arrayMSG) > 2 and ('okb' in command or 'obk' in command):
		IRCsocks[inMSG[2]].send('omode ' + inMSG[3] + ' ' + plusOrMinus + 'b ' + arrayMSG[2] + '\r\n')
	else:
		IRCsocks[inMSG[2]].send('omode ' + inMSG[3] + ' ' + plusOrMinus + 'b ' + arrayMSG[1] + '\r\n')
	if 'obk' in arrayMSG[0]: irc_kick(inMSG)

def irc_kill(inMSG):
	if inMSG[1] != 'irc' or getPermission(inMSG) < 507: return
	arrayMSG = inMSG[0].split(None, 2)
	if len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('kill ' + arrayMSG[1] + '\r\n')
	elif len(arrayMSG) > 2:
		IRCsocks[inMSG[2]].send('kill ' + arrayMSG[1] + ' :' + arrayMSG[2] + '\r\n')

def irc_kline(inMSG):
	if inMSG[1] != 'irc' or getPermission(inMSG) < 508: return
	arrayMSG = inMSG[0].split(None, 2)
	lArrayMSG = inMSG[0].split(None, 3)
	if len(arrayMSG) == 2:
		IRCsocks[inMSG[2]].send('kline 999999999 ' + arrayMSG[1] + ' :No reason specified.\r\n')
	elif len(lArrayMSG) > 3:
		IRCsocks[inMSG[2]].send('kline ' + arrayMSG[2] + ' ' + arrayMSG[1] + ' :' + arrayMSG[3] +
			'\r\n')
	
def load():
	return {'oop':(lambda x:irc_oset(x, '+o')), 'odop':(lambda x:irc_oset(x, '-o')),
		'ohop':(lambda x:irc_oset(x, '+h')), 'odhop':(lambda x:irc_oset(x, '-h')),
		'okick':irc_okick, 'oban':irc_okickban, 'ounban':(lambda x:irc_okickban(x, '-')),
		'okb':irc_okickban, 'obk':irc_okickban, 'ovoice':(lambda x:irc_oset(x, '+v')),
		'odvoice':(lambda x:irc_oset(x, '-v')), 'oadmin':(lambda x:irc_oset(x, '+a')),
		'odadmin':(lambda x:irc_oset(x, '-a')), 'god':(lambda x:irc_oset(x, '+M')),
		'mortal':(lambda x:irc_oset(x, '-M')), 'omod':(lambda x:irc_oset(x, '+m')),
		'odmod':(lambda x:irc_oset(x, '-m')), 'kill':irc_kill, 'kline':irc_kline}
