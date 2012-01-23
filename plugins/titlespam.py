import urllib2
plugName = 'Title Spam'

#Only supports Niconico atm
def titlespam_spamTitle(inMSG):
        if not inMSG or (not 'niconico.com/watch/' in inMSG[0]:
                return
        splitMSG = inMSG[0].split()
        url = ''
        for i in splitMSG:
                if 'niconico.com/watch/' in i:
                        url = i
                        break
        try:
                data = urllib2.urlopen(url).read()
        except:
                return
        try:
                pos = data.index('title" content="')+16
        except:
                return
        title = data[pos:data[pos:].index('"')+pos]
        pos = data[pos:].index('description" content="')+22+pos
        description = data[pos:data[pos:].index('"')+pos].replace('\n', ' ').replace(
                      '&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace(
                      '&gt;', '>').replace('&#039;', '\'')
        if len(description) > 50:
                description = description[:50] + '...'
        sendMSG('\x02' + title + '\x02 - ' + description, inMSG[1], inMSG[2], inMSG[3])
        
def load():
        return titlespam_spamTitle
        
