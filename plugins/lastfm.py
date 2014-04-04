#Inspired by the SkyBot plugin: https://github.com/rmmh/skybot/blob/master/plugins/lastfm.py
from json import loads
from urllib2 import urlopen
from urllib import urlencode

plugName = 'LastFM'

#put this in the DB, handle it there
lastfm_apikey = ''

def lastfm_lastfm(inMSG):
  msg = inMSG[0].split()
  if len(msg) != 2:
    return 'Usage: ' + funcPrefix + 'lastfm <user>'

  response = loads(urlopen('http://ws.audioscrobbler.com/2.0/?format=json&'+
     urlencode({'method':'user.getrecenttracks', 'api_key':lastfm_apikey, 'user':msg[1]})).read())
  
  if 'error' in response:
    return 'Error: %s' % response['message']

  if not "track" in response["recenttracks"] or len(response["recenttracks"]["track"]) == 0:
    return 'No recent tracks for \''+inMSG[1]+'\' found.'

  tracks = response["recenttracks"]["track"]

  if type(tracks) == list:
    track = tracks[0]
    status = 'current song'
  elif type(tracks) == dict:
    track = tracks
    status = 'last song'
  else:
    return 'Error parsing song listing.'

  return msg[1]+'\'s '+status+': '+track['name']+' by '+track['artist']['#text']+' on '+track['album']['#text']+'.'

def load():
  return {'lastfm':lastfm_lastfm}
