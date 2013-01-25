plugName = 'Status'

def status_status(inMSG):
    if getPermission(inMSG) < 999:
        return
    
    proto = []

    for i in protocols.items():
        proto.append(i[0])

    output = []
    output.append('Status for %s active protocols:' % (len(proto)))

    for i in proto:
        if i == 'irc':
            output.append('   * IRC, %s servers:' % (len(IRCconnections)))
            for ii in IRCconnections:
                output.append('      - %s, %s channels' % (ii[0][0], len(ii[1].split(','))))
        elif i == 'xmpp':
            connections = len(xmpp_connections)
            output.append('   * XMPP, %s servers:' % (connections))
            for ii in xrange(connections):
                ppl = xmpp_roster[ii].getItems()
                if ppl:
                    output.append('      - %s, %s friends' % (xmpp_connections[ii][0][0], len(ppl)))
                else:
                    output.append('      - %s, disconnected' % (xmpp_connections[ii][0][0]))
        elif i == 'furc':
            output.append('   * Furcadia, %s connections.' % (len(furc_sock)))

    for i in output:
        sendMSG(i, inMSG[1], inMSG[2], inMSG[3])

def load():
    return {'status':status_status}
