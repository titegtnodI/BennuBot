import Skype4Py

plugName = 'Skype'
plugAdmins = {'skype':[['titegtnodi', 1000]]}

skype_die = False

class skype_sendHandler(threading.Thread):
  def run(self):
    global outMSG
    while not skype_die:
      if len(outMSG) == 0:
        time.sleep(0.05)
      else:
        localMSG = []
        for i in outMSG:
          localMSG.append(i)
          for i in xrange(len(localMSG)):
            if len(localMSG[i]) > 1 and localMSG[i][1] == 'skype':
              localMSG[i][2].SendMessage(localMSG[i][0])
              outMSG.remove(localMSG[i])

class skype_recv(object):
  def __init__(self):
    self.skype = Skype4Py.Skype(Events=self)
    self.skype.FriendlyName = nick
    self.skype.Attach()

  def AttachmentStatus(self, status):
    if status == Skype4Py.apiAttachAvailable:
      self.skype.Attach()

  def MessageStatus(self, msg, status):
    if status == Skype4Py.cmsReceived:
      if msg.Chat.Type in (Skype4Py.chatTypeDialog, Skype4Py.chatTypeLegacyDialog, 'MULTICHAT'):
        user = msg._GetSender()
        inMSG.append([unicode(msg.Body), 'skype', msg.Chat, msg.Chat.Name, user._GetDisplayName(), user.Handle])
      msg.MarkAsSeen()

def skype_commandHandler(inMSG):
  return

def load():
  bot = skype_recv()
  skype_sendHandler().start()
  return {'skype':skype_commandHandler}
