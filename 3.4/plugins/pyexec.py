plugName = 'Local Python Exec'

def localPythonExec(inMSG):
    if getPermission(inMSG) < 1000:
        return 'Not authorized.'
    try:
        exec(inMSG[0].split(None, 1)[1])
        return 'Done.'
    except Exception as e:
        return str(e)

def load():
    return {'pyexec':localPythonExec}
