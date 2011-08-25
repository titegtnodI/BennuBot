import threading, time, socket
#BennuBot V1.0.2
#TODO Garbage collection for unused "outMSG" data.
#TODO Make general functions call every loop and let them handle timeouts.
#TODO Clean up plugins
#TODO Permissions instead of just admins

#CONSTANTS #TODO Stop using constants
PROTOCOLS = ['protocols/irc.py'] #Protocols to be loaded
PLUGINS   = ['plugins/say.py', 'plugins/mysql_poller.py', 'plugins/pyexec.py'] #Plugins to be loaded

#GLOBALS
nick = 'BennuBot'

quiet = True
funcPrefix = '.'
protoPrefix = ';'

admins = {}
funcs = {}
genFuncs = []
protocols = {}

plugName = None
load = None
plugAdmins = None

#MSG, Protocol, Server, Channel, Nick, UID (May be "None")
inMSG = []
#MSG, Protocol, Server, Channel (May be "None")
outMSG = []

#TODO
#Timestamp
#Optional print
#Log to file
def log(text):
	try: print text
	except: None

#Load all protocols from "PROTOCOLS".
def loadProtocols():
	global protocols, plugName, load, plugAdmins, admins
	protocols = {}
	for i in PROTOCOLS:
		plugName = None
		load = None
		plugAdmins = None
		try:
			eval(compile(open(i, 'U').read(), i, 'exec'), globals())
			if plugName: i = plugName
			if not load:
				log('Protocol \"' + i + '\" must define \'load\'.')
				continue
			protocols = dict(protocols.items() + load().items())
			try:
				admins = dict(admins.items() + plugAdmins.items())
			except:
				log('Protocol \"' + i + '\" has not specified any admins.')
			log('Protocol \"' + i + '\" loaded.')
		except:
			log('Protocol \"' + i + '\" failed to load.')

#Load all plugins from "PLUGINS".
def loadPlugins():
	global funcs, genFuncs, plugName, load
	funcs = {}
	genFuncs = []
	for i in PLUGINS:
		plugName = None
		load = None
		try:
			eval(compile(open(i, 'U').read(), i, 'exec'), globals())
			if plugName: i = plugName
			if not load:
				log('Plugin \"' + i + '\" must define \'load\'.')
				continue
			plugin = load()
			if type(plugin).__name__ == 'dict':
				funcs = dict(funcs.items() + plugin.items())
			elif type(plugin).__name__ == 'function':
				genFuncs += [plugin]
			else:
				log('Plugin \"' + i + '\" must return \'dict\' or \'function\'.')
				continue
			log('Plugin \"' + i + '\" loaded.')
		except:
			log('Plugin \"' + i + '\" failed to load.')

def isAdmin(inMSG):
	try:
		if not inMSG[5] in admins[inMSG[1]]:
			return False
	except:
		return False
	return True

#Parses a command.
class parseCommand(threading.Thread):

	def __init__(self, command):
		self.command = command
		threading.Thread.__init__(self)

	def run(self):
		global outMSG
		if len(self.command[0]) > 1 and self.command[0][0] == funcPrefix:
			try:
				funcs[self.command[0].split()[0][1:].lower()](self.command)
			except:
				if not quiet:
					outMSG += [['Invalid command.', self.command[1], self.command[2],
						self.command[3]]]
		elif len(self.command[0]) > 1 and self.command[0][0] == protoPrefix:
			if not isAdmin(self.command):
				if not quiet:
					outMSG += [['Not authorized.', self.command[1], self.command[2],
							self.command[3]]]
				return	
			try:
				protocols[self.command[0].split()[0][1:].lower()](self.command)
			except:
				if not quiet:
					outMSG += [['Invalid command.', self.command[1], self.command[2],
						self.command[3]]]
		else:
			for i in genFuncs:
				try:
					i(self.command)
				except:
					#TODO Output function name which had the error.
					outMSG += [['A plugin had an error.', self.command[1], self.command[2],
						self.command[3]]]

log('Loading Protocols...')
loadProtocols()
log('Loading Plugins...')
loadPlugins()

while True:
	change = False
	for i in inMSG:
		if not change: change = True
		parseCommand(i).start()
		del inMSG[0]
	if not change: time.sleep(.01)
