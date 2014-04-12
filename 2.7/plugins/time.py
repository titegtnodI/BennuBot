plugName = 'Time'
#Written by lembas for skybot
#Ported to BennuBot by titegtnodI
import datetime, random
from pytz import timezone

def time_time(inMSG):
	gmt = datetime.datetime.now(timezone("UTC")).strftime("%H:%M")
	est = datetime.datetime.now(timezone("US/Eastern")).strftime("%H:%M")
	cst = datetime.datetime.now(timezone("US/Central")).strftime("%H:%M")
	pst = datetime.datetime.now(timezone("US/Pacific")).strftime("%H:%M")
	mst = datetime.datetime.now(timezone("US/Mountain")).strftime("%H:%M")
	art = datetime.datetime.now(timezone("America/Buenos_Aires")).strftime("%H:%M")
	syd = datetime.datetime.now(timezone("Australia/Sydney")).strftime("%H:%M")
	nz = datetime.datetime.now(timezone("Pacific/Auckland")).strftime("%H:%M")
	cest = datetime.datetime.now(timezone("Europe/Berlin")).strftime("%H:%M")
	eet = datetime.datetime.now(timezone("Europe/Istanbul")).strftime("%H:%M")
	hkt = datetime.datetime.now(timezone("Asia/Hong_Kong")).strftime("%H:%M")

	sendMSG("\x0305Times:\x0f " +
		"\x0302GMT\x0f: \x0303" + gmt + "\x0f" +
			" \x0301|\x0f " +
		"\x0302PST\x0f: \x0314" + pst + "\x0f" +
			" \x0301|\x0f " +
		"\x0302MST\x0f: \x0304" + mst + "\x0f" +
			" \x0301|\x0f " +
		"\x0302CST\x0f: \x0306" + cst + "\x0f" +
			" \x0301|\x0f " +
		"\x0302EST\x0f: \x0311" + est + "\x0f" +
			" \x0301|\x0f " +
		"\x0302ART\x0f: \x0308" + art + "\x0f" +
			" \x0301|\x0f " +
		"\x0302CEST\x0f: \x0310" + cest + "\x0f" +
			" \x0301|\x0f " +
		"\x0302EET\x0f: \x0312" + eet + "\x0f" +
			" \x0301|\x0f " +
		"\x0302AWST\x0f: \x0305" + hkt + "\x0f" +
			" \x0301|\x0f " +
		"\x0302AEST\x0f: \x0307" + syd + "\x0f" +
			" \x0301|\x0f " +
		"\x0302NZST\x0f: \x0313" + nz + "\x0F"
	, inMSG[1], inMSG[2], inMSG[3])

def time_tiem(inMSG):
	gmt,est,cst,pst,mst,art,syd,nz,cest,eet,hkt = [str(random.randrange(0,3)) + str(random.randrange(0,10)) + ":" + str(random.randrange(0,6)) + str(random.randrange(0,10)) for i in xrange(11)]

	sendMSG("\x0305Times:\x0f " +
		"\x0302GMT\x0f: \x0303" + gmt + "\x0f" +
			" \x0301|\x0f " +
		"\x0302PST\x0f: \x0314" + pst + "\x0f" +
			" \x0301|\x0f " +
		"\x0302MST\x0f: \x0304" + mst + "\x0f" +
			" \x0301|\x0f " +
		"\x0302CST\x0f: \x0306" + cst + "\x0f" +
			" \x0301|\x0f " +
		"\x0302EST\x0f: \x0311" + est + "\x0f" +
			" \x0301|\x0f " +
		"\x0302ART\x0f: \x0308" + art + "\x0f" +
			" \x0301|\x0f " +
		"\x0302CEST\x0f: \x0310" + cest + "\x0f" +
			" \x0301|\x0f " +
		"\x0302EET\x0f: \x0312" + eet + "\x0f" +
			" \x0301|\x0f " +
		"\x0302AWST\x0f: \x0305" + hkt + "\x0f" +
			" \x0301|\x0f " +
		"\x0302AEST\x0f: \x0307" + syd + "\x0f" +
			" \x0301|\x0f " +
		"\x0302NZST\x0f: \x0313" + nz + "\x0F"
	, inMSG[1], inMSG[2], inMSG[3])

def load():
	return {'time':time_time, 'tiem':time_tiem}
