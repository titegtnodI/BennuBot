#Don't care if factoids isn't a word.
#Enjoy the plugin.
#TODO Implement <action> better
#TODO Implement $inp$
plugName = 'Factoids'

fact_prefix = '\''
fact_setPermissions = 0 #Permissions required to set factoids
fact_usePermissions = 0 #Permissions required to use set factoids

def fact_remember(inMSG):
    if getPermission(inMSG) < fact_setPermissions:
        return

    splitMSG = inMSG[0].split(None, 2)
    if len(splitMSG) != 3:
        return

    if getSetting('Facts', splitMSG[1]):
        return 'Factoid "'+splitMSG[1]+'" already exists.'

    if len(splitMSG[2]) < 9 or (splitMSG[2][:7] != '<reply>' and (splitMSG[2][:8] != '<action>' or
       inMSG[1] != 'irc')):
        return 'Factoid doesn\'t begin with "<reply>".'

    setSetting('Facts', splitMSG[1], (splitMSG[2],))
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

    if not getSetting('Facts', splitMSG[1]):
        return 'Factoid "'+splitMSG[1]+'" does not exist.'

    if len(splitMSG[2]) < 9 or (splitMSG[2][:7] != '<reply>' and (splitMSG[2][:8] != '<action>' or
       inMSG[1] != 'irc')):
        return 'Factoid doesn\'t begin with "<reply>".'

    setSetting('Facts', splitMSG[1], (splitMSG[2],))
    return '"'+splitMSG[1]+'" replaced.'

def fact_getFact(inMSG):
    if (not inMSG or len(inMSG) != 6 or getPermission(inMSG) < fact_usePermissions or
        len(inMSG[0]) < len(fact_prefix)+1 or inMSG[0][:len(fact_prefix)] != fact_prefix):
        return

    #TODO Check for whitespace instead, probably less intensive
    splitMSG = inMSG[0].split()
    if len(splitMSG) != 1:
        return
    
    fact = getSetting('Facts', inMSG[0][len(fact_prefix):])
    if not fact or len(fact[0][1]) < 9 or (fact[0][1][:7] != '<reply>' and (fact[0][1][:8] != '<action>' or
       inMSG[1] != 'irc')):
        return

    if fact[0][1][:2] == '<a':
        sendMSG('\x01ACTION ' + fact[0][1][8:] + '\x01', inMSG[1], inMSG[2], inMSG[3])
    else:
        return sendMSG(fact[0][1][7:], inMSG[1], inMSG[2], inMSG[3])

def load():
    global funcs
    funcs = dict(funcs.items() + [('rem',fact_remember), ('rep',fact_replace), ('f',fact_forget)])
    return fact_getFact
