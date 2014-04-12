#Don't care if factoids isn't a word.
#Enjoy the plugin!
#TODO Implement "|"
#TODO Restructure to detect who set the factoid, and maybe to support additional information
plugName = 'Factoids'

fact_prefix = '\''
fact_setPermissions = 0 #Permissions required to set factoids
fact_usePermissions = 0 #Permissions required to use set factoids

def fact_isValid(msg, protocol):
    if len(msg) < 9:
        return 'Factoid too short.'
    elif msg[:7] != '<reply>':
        if protocol == 'irc' or protocol == 'furc':
            if msg[:8] == '<action>':
                return True
            else:
                return 'Factoid doesn\'t begin with "<reply>" or "<action>".'
        else:
            return 'Factoid doesn\'t begin with "<reply>".'
    return True

def fact_getResponse(msg, protocol):
    if msg[:7] != '<reply>' and msg[:8] == '<action>':
        if protocol == 'irc':
            return '\x01ACTION ' + msg[8:] + '\x01'
        elif protocol == 'furc':
            return ':' + msg[8:]
    else:
        return msg[7:]
    return False

def fact_remember(inMSG):
    if getPermission(inMSG) < fact_setPermissions:
        return

    splitMSG = inMSG[0].split(None, 2)
    if len(splitMSG) != 3:
        return

    conn = sqlite3.connect(dbLoc)

    if getSetting('Facts', splitMSG[1], conn):
        conn.close()
        return 'Factoid "'+splitMSG[1]+'" already exists.'

    validResponse = fact_isValid(splitMSG[2], inMSG[1])

    if validResponse != True:
        conn.close()
        return validResponse

    setSetting('Facts', splitMSG[1], (splitMSG[2],), ('Value',), conn)
    conn.close()
    return '"'+splitMSG[1]+'" added.'

def fact_forget(inMSG):
    if getPermission(inMSG) < fact_setPermissions:
        return

    splitMSG = inMSG[0].split()
    if len(splitMSG) != 2:
        return

    if not delSetting('Facts', splitMSG[1]):
        return 'Error deleting "'+splitMSG[1]+'" (Probably doesn\'t exist).'

    return '"'+splitMSG[1]+'" deleted.'

def fact_replace(inMSG):
    if getPermission(inMSG) < fact_setPermissions:
        return

    splitMSG = inMSG[0].split(None, 2)
    if len(splitMSG) != 3:
        return

    conn = sqlite3.connect(dbLoc)

    if not getSetting('Facts', splitMSG[1], conn):
        conn.close()
        return 'Factoid "'+splitMSG[1]+'" does not exist.'

    validResponse = fact_isValid(splitMSG[2], inMSG[1])

    if validResponse != True:
        conn.close()
        return validResponse

    setSetting('Facts', splitMSG[1], (splitMSG[2],), ('Value',), conn)
    conn.close()
    return '"'+splitMSG[1]+'" replaced.'

def fact_getFact(inMSG):
    if (not inMSG or len(inMSG) != 6 or getPermission(inMSG) < fact_usePermissions or
        len(inMSG[0]) < len(fact_prefix)+1 or inMSG[0][:len(fact_prefix)] != fact_prefix):
        return

    splitMSG = inMSG[0].split()
    if len(splitMSG) > 2:
        return
    elif len(splitMSG) == 2:
        who = splitMSG[1]
    else:
        who = inMSG[4]
    
    fact = getSetting('Facts', splitMSG[0][len(fact_prefix):])

    if fact:
        validResponse = fact_isValid(fact[0][1], inMSG[1])
    else:
        return

    if validResponse != True:
        sendMSG(validResponse, inMSG[1], inMSG[2], inMSG[3])

    validResponse = fact_getResponse(fact[0][1], inMSG[1])

    if validResponse:
        sendMSG(validResponse.replace('$inp$', who), inMSG[1], inMSG[2], inMSG[3])

def load():
    global funcs
    funcs = dict(funcs.items() + [('rem',fact_remember), ('rep',fact_replace), ('f',fact_forget)])
    return fact_getFact
