#Responses taken from: https://github.com/lahwran/skybot/blob/master/plugins/8ball.py

import random

eightball_answers = ["As I see it, yes", "It is certain", "It is decidedly so", "Most likely",
                 "Outlook good", "Signs point to yes", "Without a doubt", "Yes", "Yes, definitely", 
                 "You may rely on it", "Reply hazy, try again", "Ask again later",
                 "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                 "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good",
                 "Very doubtful"]

def eightball_guess(inMSG):
  if len(inMSG[0].split()) < 2:
    return 'Usage: '+funcPrefix+'8ball <question>'
  return eightball_answers[random.randint(0, len(eightball_answers)-1)]

def load():
  return {'8ball':eightball_guess}
