import random

#This plugin should probably never be used for any reason
plugName = 'Awful'

awful_frequency = 15
awful_last = 0

awful_negative = ['not', 'isn\'t']
awful_insults = {'mother':[['mother', 'dead'], ['Good.', 'Never liked her anyways.']],
'generic':[[' wide', 'did it', 't was quick', ' huge'],
['Wide like your mother\'s vagina?', 'Like I did your mother?', 'That\'s what she said.', 'Huge like my massive penis?']]}

def awful_findMatch(phrase, alist):
  for i in alist:
    if i in phrase:
      return alist.index(i)
  return False

def awful_awful(inMSG):
  global awful_last
  if time.time() - awful_frequency < awful_last or not inMSG:
    return

  msg = inMSG[0].lower()
  out = None

  if type(awful_findMatch(msg, awful_negative)) == bool:
    if awful_insults['mother'][0][0] in msg and awful_insults['mother'][0][1] in msg:
      out = awful_insults['mother'][1][random.randint(0, 1)]
    elif type(awful_findMatch(msg, awful_insults['generic'][0])) != bool:
      out = awful_insults['generic'][1][awful_findMatch(msg, awful_insults['generic'][0])]

  if out:
    awful_last = time.time()
    sendMSG(out, inMSG[1], inMSG[2], inMSG[3])

def load():
  return awful_awful