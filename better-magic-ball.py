from __future__ import unicode_literals, absolute_import, print_function, division
from nltk.corpus import stopwords
import re, random, time

STOPWORDS = set(stopwords.words('english'))

NUMVALUES = {"a":1,"j":1,"s":1,"b":2,"k":2,"t":2,"c":3,"l":3,"u":3,"d":4,"m":4,"v":4,
             "e":5,"n":5,"w":5,"f":6,"o":6,"x":6,"g":7,"p":7,"y":7,"h":8,"q":8,"z":8,
             "i":9,"r":9}

EIGHTBALL = ("It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
             "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
             "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
             "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don't count on it.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Very doubtful.")

TIMEFRAME = 300 # Number of seconds of stability the prediction will have.

def get_numerological_value(word):
   # https://en.wikipedia.org/wiki/Numerology#Latin_alphabet_systems
   digits = str(sum([NUMVALUES[l] for l in word.lower() if l in NUMVALUES.keys()]))
   value = int(digits) % 9
   if value == 0:
      value = 9
   return value

def get_answer_to_question(question):
   # Strip junk and junk words, get rng seed from numerological sum, then weight against current time.
   words = list(filter(lambda word: word not in STOPWORDS, re.sub("[^a-z0-9 ]+", "", question.lower()).split()))
   total = sum(get_numerological_value(word) for word in words)
   random.seed(total + int(time.time()/TIMEFRAME))
   answer = random.choice(EIGHTBALL)
   return answer

try:
   import sopel.module
except ImportError:
   pass
else:
   @sopel.module.commands('q')
   @sopel.module.example('.q some question')
   def f_ask_question(bot, trigger):
     """Ask the Magic 8 ball a question weighted with Latin numerology."""
     if trigger.group(2):
         phrase = re.sub('[^a-zA-Z ]', '', trigger.group(2)).strip().lower()
         results = get_definitions(phrase)
         if results and len(results):
             definitions = ". " .join(["{} {}".format(underline(pair[0]), pair[1]) for pair in results])
             bot.say(definitions, trigger.sender, len(definitions)*2)
         else:
             bot.say('Can\'t find the etymology for "{}".'.format(phrase), trigger.sender)
     return sopel.module.NOLIMIT

if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
      query = ' '.join(sys.argv[1:])
      answer = get_answer_to_question(query)
      print('Answer: {}'.format(answer))
   else:
      print("{}: No question given.".format(sys.argv[0]))
