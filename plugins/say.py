plugName = 'Say'

def say_say(inMSG):
    msg = inMSG[0].split(None, 1)
    if len(msg) > 1:
        return msg[1]
    else:
        return 'Usage: ' + funcPrefix + 'say <msg>'

def say_reverse(inMSG):
    msg = inMSG[0].split(None, 1)
    if len(msg) > 1:
        return msg[1][::-1]
    else:
        return 'Usage: ' + funcPrefix + 'rev <msg>'

def load():
    return {'say':say_say, 'rev':say_reverse}
