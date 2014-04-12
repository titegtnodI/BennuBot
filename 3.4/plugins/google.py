from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
plugName = 'Google Plugin'

#TODO Descriptions

def google_search(query, method):
    return loads(urlopen('http://ajax.googleapis.com/ajax/services/search/'+method+'?v=1.0&'+
        urlencode({'q':query.encode('utf-8')})).read())

def google_firstResult(inMSG, method):
    splitMSG = inMSG[0].split(None, 1)
    if len(splitMSG) != 2:
        return 'Usage: .g <search>'
    result = google_search(inMSG[0].split(None, 1)[1], method)['responseData']['results']
    if result:
        sendMSG(result[0]['titleNoFormatting'] + ' -- ' + result[0]['unescapedUrl'],
            inMSG[1], inMSG[2], inMSG[3])
    else:
        sendMSG('No results found.', inMSG[1], inMSG[2], inMSG[3])

def load():
    return {'g':(lambda x: google_firstResult(x, 'web')), 'gi':(lambda x: google_firstResult(x, 'images'))}
