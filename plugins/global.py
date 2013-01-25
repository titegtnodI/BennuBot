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
                    sendMSG(splitMSG[2], 'irc', ii, iii)
        elif i == 'xmpp':
            for ii in xrange(len(xmpp_connections)):
                if not xmpp_roster[ii]: continue
                ppl = xmpp_roster[ii].getItems()
                for iii in ppl:
                    sendMSG(splitMSG[2], 'xmpp', ii, iii)
        elif i == 'furc':
            for ii in xrange(len(furc_sock)):
                sendMSG(splitMSG[2], 'furc', ii, '')

def load():
    return {'global':global_send}
