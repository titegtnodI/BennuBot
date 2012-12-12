plugName = 'Global Messenger'

def global_send(inMSG):
    if getPermission(inMSG) != 1000:
        return
    splitMSG = inMSG[0].split(None, 2)
    if len(splitMSG) != 3:
        return 'Usage: '+funcPrefix+'global <protocols (comma sep)> <msg>'
    
    protocols = splitMSG[1].split(',')

    for i in protocols:
        if i == 'irc':
            for ii in xrange(len(IRCconnections)):
                channels = IRCconnections[ii][1].split(',')
                for iii in channels:
                    IRCsocks[ii].send('PRIVMSG ' + iii + ' :' + splitMSG[2] + '\r\n')
        elif i == 'xmpp':
            for ii in xrange(len(xmpp_connections)):
                ppl = xmpp_roster[ii].getItems()
                for iii in ppl:
                    xmpp_jabber[ii].send(xmpp.Message(iii, splitMSG[2]))

def load():
    return {'global':global_send}
