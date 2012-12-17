import re, htmlentitydefs
plugName = 'Furcadia'
plugAdmins = {'furc':[['titegtnodi',1000]]}

furc_connections = [['furc://titegtnodi:pho3n1x', 'doop', 'password', ['"Hello everyone!']]]

furc_die = False
furc_debug = True

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
# All credits for this function go to Fredrik Lundh
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

class furc_sendHandler(threading.Thread):

    def run(self):
        global outMSG
        while not furc_die:
            if len(outMSG) == 0:
                time.sleep(0.05)
            else:
                localMSG = []
                for i in outMSG:
                    localMSG.append(i)
                for i in xrange(len(localMSG)):
                    if len(localMSG[i]) > 1 and localMSG[i][1] == 'furc':
                        if localMSG[i][3] != '':
                            furc_sock[localMSG[i][2]].send(('wh ' + localMSG[i][3] + ' ' + localMSG[i][0] + '\n').encode('utf-8'))
                        else:
                            furc_sock[localMSG[i][2]].send(('"' + localMSG[i][0] + '\n').encode('utf-8'))
                        outMSG.remove(localMSG[i])

class furc_connectionHandler(threading.Thread):

    def __init__(self, i):
        self.i = i
        threading.Thread.__init__(self)

    def run(self):
        global furc_sock, inMSG
        while not furc_die:
            furc_sock[self.i] = socket.socket()
            furc_sock[self.i].settimeout(240)
            try:
                furc_sock[self.i].connect(('lightbringer.furcadia.com', 2300))
                last_time = time.time()
                trail_msg = ''
                msg = []
                while last_time+240 > time.time() and 'Dragonroar' not in msg:
                    data = trail_msg + furc_sock[self.i].recv(256)
                    msg = data.split('\n')
                    if data[-1] != '\n':
                        trail_msg = data[-1]
                        if len(msg) > 0:
                            del msg[-1]
                    time.sleep(.1)
                            
                furc_sock[self.i].send('connect ' + furc_connections[self.i][1].replace(' ', '|') + ' ' +
                                       furc_connections[self.i][2] + '\n')
                time.sleep(0.5)
                furc_sock[self.i].send('desc BennuBot! Find out more at http://titegtnodi.github.com/BennuBot\n')
                
                last_time = time.time()
                while last_time+240 > time.time() and '&&&&&&&&&&&&&' not in msg:
                    data = trail_msg + furc_sock[self.i].recv(256)
                    msg = data.split('\n')
                    if data[-1] != '\n':
                        trail_msg = data[-1]
                        if len(msg) > 0:
                            del msg[-1]
                    time.sleep(.1)
                            
                furc_sock[self.i].send('color t#############\n')
                time.sleep(1)
                furc_sock[self.i].send('fdl ' + furc_connections[self.i][0] + '\n')
                time.sleep(1)
                furc_sock[self.i].send('vascodagama\n')
                for i in furc_connections[self.i][3]:
                    time.sleep(0.8)
                    furc_sock[self.i].send(i + '\n')
                
            except Exception as e:
                if furc_debug:
                    print '[Furc-Err]\t%s' % (e)
                continue
                
            last_keepalive = time.time()
            while not furc_die:
                #Make sure we don't logout from inactivity
                if last_keepalive+5 <= time.time():
                    try:
                        furc_sock[self.i].send('iamhere\n')
                    except:
                        #So we reconnect if the socket dies
                        break
                    last_keepalive = time.time()+5
                    
                try:
                    data = trail_msg + furc_sock[self.i].recv(256)
                except:
                    #So we reconnect if the socket dies
                    break
                msg = data.split('\n')
                if data[-1] != '\n':
                    trail_msg = data[-1]
                    if len(msg) > 0:
                        del msg[-1]
                        
                #Loop through all the message
                for i in msg:
                    if i.startswith('(<name shortname='):
                        line = i[18:]
                        uid = line[:line.index('\'')]
                        line = line[len(uid)+2:]
                        name = line[:line.index('<')]
                        line = line[len(name)+9:]
                        inMSG.append([unescape(line).decode('utf-8'), 'furc', self.i, '', name, uid])
                    elif i[1:].startswith('(<font color=\'whisper\'>[ <'):
                        line = i[43:]
                        uid = line[:line.index('\'')]
                        line = line[len(uid)+21:]
                        name = line[:line.index('<')]
                        line = line[len(name)+19:]
                        line = line[:line.index('"')]
                        inMSG.append([unescape(line).decode('utf-8'), 'furc', self.i, name.replace(' ', '|'), name, uid])
                        
        try:
            furc_sock[self.i].send('quit\n')
        except:
            None

def furc_commandHandler(inMSG):
    global furc_die
    
    msg = inMSG[0].split(None, 2)
    if msg[1] == 'raw':
        furc_sock[inMSG[2]].send(msg[2] + '\n')
    elif msg[1] == 'die':
        furc_die = True
    elif msg[1] == '3':
        furc_sock[inMSG[2]].send('m 3\n')
    elif msg[1] == '7':
        furc_sock[inMSG[2]].send('m 7\n')
    elif msg[1] == '1':
        furc_sock[inMSG[2]].send('m 1\n')
    elif msg[1] == '9':
        furc_sock[inMSG[2]].send('m 9\n')
        
def load():
    global furc_sock, furc_die
    #If connections exists, close them
    furc_die = True
    try:
        for i in furc_sock:
            i.send('quit\n')
            time.sleep(1)
    except:
        None
    furc_die = False
    furc_sock = []
    #Setup all connections for multiple servers
    for i in xrange(len(furc_connections)):
        furc_sock += [None]
        furc_connectionHandler(i).start()
        time.sleep(.1)
    furc_sendHandler().start()
    return {'furc':furc_commandHandler}
