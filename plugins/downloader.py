import random
#Depends on plugin "Google"
plugName = 'Downloader'

#TODO Torrents

def downloader_get(inMSG):
	query = inMSG[0].split(None, 1)[1].lower()
	qSet = set(query.split())
	sites = ['mediafire.com', 'filetram.com']
	msg = []
	for i in sites:
		time.sleep((random.randint(100, 250) + .0) / 100)
		search = google_search('site:'+i+' ' + query, 'web')['responseData']['results']
		if search:
			if '.' in search[0]['titleNoFormatting']:
				dotTitle = set(search[0]['titleNoFormatting'].lower().split('.'))
			else:
				dotTitle = None
			if set(search[0]['titleNoFormatting'].lower().split()).intersection(qSet) or \
			(dotTitle and dotTitle.intersection(qSet)):
				msg += [search[0]['titleNoFormatting'] + '-- ' + search[0]['unescapedUrl']]
	if len(msg) > 0:
		sendMSG(' | '.join(msg).encode('utf-8'), inMSG[1], inMSG[2], inMSG[3])
	else:
		sendMSG('No results found.', inMSG[1], inMSG[2], inMSG[3])

def load():
	return {'get':downloader_get}
