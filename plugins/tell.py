plugName = 'Tell'

def tell_tell(inMSG):
        msg = inMSG[0].split(None, 2)
        if len(msg) < 3:
                return 'Usage: '+funcPrefix+'tell <nick> <msg>'

        message = getSetting('Tell', inMSG[4])
        if message and message[0][1].split('\xff') > 9:
                return msg[1] + ' has enough tells.'
        if message:
                messages = message[0][1] + '\x7f' + msg[2].replace('\'', '')
                authors = message[0][2] + '\x7f' + inMSG[4]
        else:
                messages = msg[2].replace('\'', '')
                authors = inMSG[4]

        setSetting('Tell', msg[1], {'Messages':messages, 'Authors':authors})
        sendMSG(inMSG[4] + ': I\'ll pass that along.', inMSG[1], inMSG[2], inMSG[3])

def tell_tellTells(inMSG):
        if not inMSG or len(inMSG) != 6:
                return

        message = getSetting('Tell', inMSG[4])
        if message:
                messages = message[0][1].split('\x7f')
                authors = message[0][2].split('\x7f')
                for i in xrange(len(messages)):
                        sendMSG((authors[i] + ' sent you: ' + messages[i]).encode('utf-8'), inMSG[1],
                                inMSG[2], inMSG[4])
                delSetting('Tell', inMSG[4])                

def load():
        global funcs
        funcs = dict(funcs.items() + [('tell', tell_tell)])
	return tell_tellTells
