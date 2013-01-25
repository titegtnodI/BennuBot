import os
plugName = 'Remote Admin'

def remote_shutdown(inMSG):
        if getPermission(inMSG) < 1000:
                return
        sendMSG("Shutting down...", inMSG[1], inMSG[2], inMSG[3])
        time.sleep(.5)
        log("Shutting down because of a command from "+inMSG[5])
        os._exit(0)

def remote_restart(inMSG):
        if getPermission(inMSG) < 1000:
                return
        sendMSG("Restarting...", inMSG[1], inMSG[2], inMSG[3])
        time.sleep(.5)
        log("Restarting because of a command from "+inMSG[5])
        loadSettings()
        loadProtocols()
        loadPlugins()

def remote_setSysSetting(inMSG):
        if getPermission(inMSG) < 1000:
                return
        splitMSG = inMSG[0].split(None, 2)
        if len(splitMSG) == 3:
                setSetting("System", splitMSG[1], (splitMSG[2],))
                sendMSG("Set "+splitMSG[1]+" to "+splitMSG[2], inMSG[1], inMSG[2], inMSG[3])
        else:
                sendMSG("Usage: "+funcPrefix+"setsys <var> <value>", inMSG[1], inMSG[2], inMSG[3])

def remote_reloadSettings(inMSG):
        if getPermission(inMSG) < 1000:
                return
        sendMSG("Reloading settings...", inMSG[1], inMSG[2], inMSG[3])
        time.sleep(.5)
        loadSettings()

def remote_reloadPlugins(inMSG):
        if getPermission(inMSG) < 1000:
                return
        sendMSG("Reloading plugins...", inMSG[1], inMSG[2], inMSG[3])
        loadPlugins()

def remote_reloadProtocols(inMSG):
        if getPermission(inMSG) < 1000:
                return
        sendMSG("Reloading protocols...", inMSG[1], inMSG[2], inMSG[3])
        time.sleep(.5)
        loadProtocols()

def remote_loadPlugin(inMSG):
        if getPermission(inMSG) < 1000:
                return
        plugin = inMSG[0].split()
        if len(plugin) < 2:
                return
        global plugList

        sendMSG("Loading plugin "+plugin[1]+"...", inMSG[1], inMSG[2], inMSG[3])
        if len(plugin) == 3:
                success = loadPlugin(plugin[2]+plugin[1], plugin[1])
        else:
                success = loadPlugin(plugFolder+plugin[1], plugin[1])

        if not success:
            sendMSG('Plugin "'+plugin[1]+'" failed to load.')

        #If plugin isn't autoloaded ... autoload it ... only if it actually loads
        if not plugin[1] in plugList and len(plugin) == 2 and success:
                plugList += [plugin[1]]
                setSetting("System", "plugList", (','.join(plugList),))

def remote_unloadPlugin(inMSG):
        if getPermission(inMSG) < 1000:
                return
        plugin = inMSG[0].split()
        if len(plugin) < 2:
                return
        lPlugList = plugList

        sendMSG("Unloading plugin "+plugin[1]+"...", inMSG[1], inMSG[2], inMSG[3])
        if plugin[1] in lPlugList:
                del lPlugList[lPlugList.index(plugin[1])]
                setSetting("System", "plugList", (','.join(lPlugList),))

        loadPlugins()

def remote_loadProtocol(inMSG):
        if getPermission(inMSG) < 1000:
                return
        plugin = inMSG[0].split()
        if len(plugin) < 2:
                return
        global protoList

        sendMSG("Loading protocol "+plugin[1]+"...", inMSG[1], inMSG[2], inMSG[3])
        if len(plugin) == 3:
                success = loadProtocol(plugin[2]+plugin[1], plugin[1])
        else:
                success = loadProtocol(protoFolder+plugin[1], plugin[1])

        if not success:
            sendMSG('Protocol "'+plugin[1]+'" failed to load.')

        #If plugin isn't autoloaded ... autoload it ... only if it actually loads
        if not plugin[1] in protoList and len(plugin) == 2 and success:
                protoList += [plugin[1]]
                setSetting("System", "protoList", (','.join(protoList),))

def remote_unloadProtocol(inMSG):
        if getPermission(inMSG) < 1000:
                return
        plugin = inMSG[0].split()
        if len(plugin) < 2:
                return
        lPlugList = protoList

        sendMSG("Unloading protocol "+plugin[1]+"...", inMSG[1], inMSG[2], inMSG[3])
        if plugin[1] in lPlugList:
                del lPlugList[lPlugList.index(plugin[1])]
                setSetting("System", "protoList", (','.join(lPlugList),))

        loadProtocols()

def load():
	return {'shutdown':remote_shutdown, 'restart':remote_restart, 'setsys':remote_setSysSetting,
                'settings':remote_reloadSettings, 'plugins':remote_reloadPlugins,
                'protocols':remote_reloadProtocols, 'plugin':remote_loadPlugin,
                'rmplugin':remote_unloadPlugin, 'protocol':remote_loadProtocol,
                'rmprotocol':remote_unloadProtocol}
