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
        print splitMSG
        if len(splitMSG) == 3:
                setSetting("System", splitMSG[1], {"Value":splitMSG[2]})
                sendMSG("Set "+splitMSG[1]+" to "+splitMSG[2], inMSG[1], inMSG[2], inMSG[3])
        else:
                sendMSG("Usage: .setsys <var> <value>")

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

def load():
	return {'shutdown':remote_shutdown, 'restart':remote_restart, 'setsys':remote_setSysSetting,
                'settings':remote_reloadSettings, 'plugins':remote_reloadPlugins,
                'protocols':remote_reloadProtocols}
