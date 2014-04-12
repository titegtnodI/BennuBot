import urllib2
plugName = 'Title Spam'

def titlespam_nnVideoInfo(data, tTag, dTag, case=None):
        try:
                pos = data.index(tTag)+len(tTag)
        except:
                return None, None

        if not case:
                case = tTag[-1]
        #TODO Use regex
        title = data[pos:data[pos:].index(case)+pos].replace('\\', '').replace('&quot;', '"')
        pos = data[pos:].index(dTag)+len(dTag)+pos
        description = data[pos:data[pos:].index(case)+pos].replace('\n', ' ').replace(
                      '&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace(
                      '&gt;', '>').replace('&#039;', '\'')
        if len(description) > 50:
                description = description[:50] + '...'

        return title, description

#Only supports Niconico atm
def titlespam_spamTitle(inMSG):
        if not inMSG or not 'niconico.com/watch/' in inMSG[0]:
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

        if 'video' in url:
                title, description = titlespam_nnVideoInfo(data, 'title" content="', 'description" content="')
        elif 'live' in url:
                title, description = titlespam_nnVideoInfo(data, "title:        '", "description:  '", "',")
        else:
                return

        if not title:
                return

        sendMSG('\x02' + title + '\x02 - ' + description, inMSG[1], inMSG[2], inMSG[3])
        
def load():
        return titlespam_spamTitle
