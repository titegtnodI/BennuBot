#TODO SSL
plugName = 'IRC'
plugAdmins = {'irc':['titegtnodI!~titegtnod@rainbows.inafire.com']}

#TODO Handle join fails properly.
#TODO Update channels upon kick.
#TODO Handle nick changes properly (If nick change fails).
#TODO Announce a successful ";irc die"
IRCconnections = [[('irc.pho3n1x.net', 6667), '#bottest', nick]]
IRCsocks = []
IRCdie = False

class ircSendHandler(threading.Thread):

	def run(self):
		global outMSG
		while not IRCdie:
			if len(outMSG) == 0:
				time.sleep(0.05)
			else:
				nCount = 0
				for i in xrange(len(outMSG)):
					if len(outMSG[i]) > 1 and outMSG[i][1] == 'irc':
						IRCsocks[outMSG[i][2]].send('PRIVMSG ' + outMSG[i][3] + ' :' + outMSG[i][0] + '\r\n')
						outMSG[i] = None
						nCount += 1
				index = 0
				while nCount > 0:
					if not outMSG[index]:
						del outMSG[index]
						nCount -= 1
					else:
						index += 1
				

class ircConnectionHandler(threading.Thread):

	def __init__(self, i):
		self.i = i
		threading.Thread.__init__(self)

	def run(self):
		global IRCsocks, inMSG
		while not IRCdie:
			IRCsocks[self.i] = socket.socket()
			IRCsocks[self.i].settimeout(240)
			try:
				IRCsocks[self.i].connect(IRCconnections[self.i][0])
				IRCsocks[self.i].send('USER ' + nick + ' ' + nick + ' ' + nick + ' ' + nick + '\r\n')
				IRCsocks[self.i].send('NICK ' + nick + '\r\n')
			except:
				continue
			while not IRCdie:
				try:
					data = IRCsocks[self.i].recv(256)
				except:
					break
				if data == '':
					break

				for i in xrange(len(data)):
					if i+2 >= len(data):
						msg = ''
						break
					if data[i+1] == ':':
						msg = data[i+2:-2]
						break
				if data.strip() != '':
					data = data.split()
				elif data[0] == 'PING':
					IRCsocks[self.i].send('PONG ' + data[1][1:] + '\r\n')
				elif len(data) > 1 and len(data[1]) == 3 and data[1][:3] == '001':
					IRCsocks[self.i].send('JOIN ' + IRCconnections[self.i][1] + '\r\n')
				else:
					try:
						if data[2][0] == '#':
							inMSG += [[msg, 'irc', self.i, data[2], data[0].split('!')[0][1:], data[0][1:]]]
						else:
							inMSG += [[msg, 'irc', self.i, data[0].split('!')[0][1:], data[0].split('!')[0][1:], data[0][1:]]]
					except:
						None
		IRCsocks[self.i].shutdown(socket.SHUT_RDWR)
		IRCsocks[self.i].close()

def ircCommandHandler(inMSG):
	global outMSG, IRCdie
	msg = inMSG[0].split()
	if len(msg) > 1:
		command = msg[1].lower()
	else:
		return
	if command == 'send':
		outMSG += [[inMSG[0][inMSG[0].index(msg[2])+len(msg[2])+1:], inMSG[1], inMSG[2], msg[2]]]
	elif command == 'die':
		IRCdie = True
		del protocols['irc']
	else:
		try:
			if command == 'join':
				if msg[2][0] != '#':
					msg[2] = '#' + msg[2]
				IRCsocks[inMSG[2]].send(command.upper() + ' ' + msg[2] + '\r\n')
				if IRCconnections[inMSG[2]][1] != '':
					IRCconnections[inMSG[2]][1] += ',' + msg[2]
				else:
					IRCconnections[inMSG[2]][1] = msg[2]
			elif command == 'part':
				if msg[2][0] != '#':
					msg[2] = '#' + msg[2]
				IRCsocks[inMSG[2]].send(command.upper() + ' ' + msg[2] + ' ' +
					inMSG[0][inMSG[0].index(msg[2])+len(msg[2])+1:] + '\r\n')
				chanArray = IRCconnections[inMSG[2]][1].split(',')
				if msg[2] in chanArray:
					del chanArray[chanArray.index(msg[2])]
					IRCconnections[inMSG[2]][1] = ','.join(chanArray)
			elif command == 'nick':
				IRCsocks[inMSG[2]].send(command.upper() + ' ' + msg[2] + '\r\n')
				IRCconnections[inMSG[2]][2] = msg[2]
			elif command == 'raw':
				IRCsocks[inMSG[2]].send(inMSG[0][inMSG[0].index('raw')+4:] + '\r\n')
		except:
			outMSG += [['Error.', inMSG[1], inMSG[2], inMSG[3]]]
		

def load():
	global IRCsocks
	#Setup all connections for multiple servers
	for i in xrange(len(IRCconnections)):
		IRCsocks += [None]
		ircConnectionHandler(i).start()
		time.sleep(.1)
	ircSendHandler().start()
	return {'irc':ircCommandHandler}
