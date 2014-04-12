#Depends on XMPPpy
import xmpp
plugName = 'XMPP'
plugAdmins = {'xmpp':[['sum20165069@pvp.net',1000]]}

xmpp_connections = [[('chat.na1.lol.riotgames.com', 5223), 'DroffilcTheTinyBlueDog@pvp.net', 'AIR_1k1kInyt8bb', 'xiff']]

xmpp_die = False
xmpp_roster = []
xmpp_debug = True

class xmpp_sendHandler(threading.Thread):

    def run(self):
        global outMSG
        while not xmpp_die:
            if len(outMSG) == 0:
                time.sleep(0.05)
            else:
                localMSG = []
                for i in outMSG:
                    localMSG.append(i)
                for i in xrange(len(localMSG)):
                    if len(localMSG[i]) > 1 and localMSG[i][1] == 'xmpp':
                        print 'Sent: ' + localMSG[i][3]
                        xmpp_jabber[localMSG[i][2]].send(xmpp.Message(localMSG[i][3], localMSG[i][0]))
                        outMSG.remove(localMSG[i])

def xmpp_message(sess, msg, server):
    global inMSG
    #TODO Handle shit properly so I don't need a try/except
    try:
        jid = str(msg.getFrom())
        nick = xmpp_roster[server].getName(jid)
        if not nick:
            nick = jid.split('@')[0]
        text = msg.getBody()
        print 'Got: ' + text
        if text:
            inMSG.append([unicode(text), 'xmpp', server, jid, nick, jid])
    except Exception as e:
        if xmpp_debug:
            print '[XMPP-Err]\t%s' % (e)
                
class xmpp_connectionHandler(threading.Thread):

    def __init__(self, i):
        self.i = i
        threading.Thread.__init__(self)

    def run(self):
        global xmpp_jabber, xmpp_roster, inMSG
        while not xmpp_die:
            jid = xmpp.protocol.JID(xmpp_connections[self.i][1])
            xmpp_jabber[self.i] = xmpp.Client(jid.getDomain(), debug=[])
            try:
                xmpp_jabber[self.i].connect(xmpp_connections[self.i][0])
                xmpp_jabber[self.i].auth(jid.getNode(), xmpp_connections[self.i][2],
                                         xmpp_connections[self.i][3])
                xmpp_jabber[self.i].sendInitPresence(requestRoster=1)
                xmpp_jabber[self.i].RegisterHandler('message', (lambda x,y:xmpp_message(x, y, self.i)))
            except Exception as e:
                if xmpp_debug:
                    print '[XMPP-Err]\t%s' % (e)
                continue
            last_roster = time.time()
            last_keepalive = last_roster
            while not xmpp_die and xmpp_jabber[self.i].Process(1):
                if last_roster <= time.time():
                    xmpp_roster[self.i] = xmpp_jabber[self.i].getRoster()
                    last_roster = time.time()+30
                if last_keepalive+5 <= time.time():
                    xmpp_jabber[self.i].send(xmpp.Message(xmpp_connections[self.i][1], None))
                    last_keepalive = time.time()+5
                time.sleep(0.05)
        try:
            #TODO Properly close the connection
            None
        except:
            None

def xmpp_commandHandler(inMSG):
    return
        
def load():
    global xmpp_jabber, xmpp_roster, xmpp_die
    #If connections exists, close them
    xmpp_die = True
    try:
        for i in xmpp_jabber:
            try:
                i.disconnect()
                time.sleep(0.5)
            except:
                None
    except:
        None
    xmpp_die = False
    xmpp_jabber = []
    #Setup all connections for multiple servers
    for i in xrange(len(xmpp_connections)):
        xmpp_jabber += [None]
        xmpp_roster += [None]
        xmpp_connectionHandler(i).start()
        time.sleep(.1)
    xmpp_sendHandler().start()
    return {'xmpp':xmpp_commandHandler}
