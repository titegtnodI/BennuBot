#Grabs a random image from Lolibooru ...
#This would probably work on most Booru websites
import urllib2
plugName = 'Loli Grabber'

#Tags don't work with random ... shame : /
#TODO Support tags manually
def loli_locate(tags):
    req = urllib2.Request('http://lolibooru.com/index.php?page=post&s=random&tags='+tags)
    res = urllib2.urlopen(req)
    data = res.read()
    data = data[data.index('<title>')+7:data.index('</title>')]
    return data, res.geturl()

def loli_get(inMSG):
    splitMSG = inMSG[0].split()
    if len(splitMSG) == 1:
        name, url = loli_locate('')
        sendMSG(url, inMSG[1], inMSG[2], inMSG[3])
    else:
        sendMSG("Usage: "+funcPrefix+"loli (No options supported yet...)", inMSG[1], inMSG[2], inMSG[3])

def load():
    return {'loli':loli_get}
