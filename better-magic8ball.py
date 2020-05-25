from __future__ import unicode_literals, absolute_import, print_function, division
from nltk.corpus import stopwords
from pathlib import Path
import re
import random
import time
import json


class ProphecyBase:
    """ Base class for a prophecy (which is an answer) """

    def __init__(self, oracle, significance, prophecy):
        self.oracle = oracle
        self.significance = significance
        self.prophecy = prophecy

    def get_significance(self):
        """ Gets the significance of this prophecy """
        return self.significance

    def get_oracle(self):
        """ Gets the oracle school that this prophecy belongs to """
        return self.oracle

    def get_prophecy_text(self):
        """ Gets the prophetic words of this prophecy """
        return "{}".format(self.prophecy)

    def set_prophecy_text(self, text):
        """ Sets the prophetic words of this prophecy """
        this.prophecy = text

    def __repr__(self):
        return "<Prophecy significance: {} text: '{}'".format(
            self.significance, self.get_prophecy_text()
        )


class OracleBase:
    """ Base class for a generator of prophecies """

    def __init__(self, school, oracle_name):
        """ Creates an Oracle as part of a certain School of Mythology """
        self.school = school
        self.oracle_name = oracle_name

    def get_prophecy(self, question):
        return ProphecyBase(self, 0.0, "The universe is silent")


#
#   NUMEROLOGY
#
class NumerologyProphecy(ProphecyBase):
    """ Prophecy for numerology """
    pass


class NumerologyOracle(OracleBase):

    EIGHTBALL = []

    def __init__(self, school, oracle_name):
        super().__init__(school, oracle_name)

        self.EIGHTBALL = read_json(
            "better-magic8ball.prophecies.json")["8ball"]

        if oracle_name == "Modern Numerology":
            # Apply the numerological value of the current name as the
            # significant factor for the numerology
            self.NUMEROLOGICAL_NAME_VALUE = self.get_numerological_value(
                self.oracle_name)

            # Create a square to adjust the timeframe for our name
            epoch_time = int(time.time() * 100000)

            if epoch_time % 2 == 0:
                self.NUMEROLOGICAL_NAME_VALUE *= 1.0
            else:
                self.NUMEROLOGICAL_NAME_VALUE *= -1.0

            if self.NUMEROLOGICAL_NAME_VALUE % 2 == 0:
                self.TIMEFRAME += self.NUMEROLOGICAL_NAME_VALUE
            else:
                self.TIMEFRAME -= self.NUMEROLOGICAL_NAME_VALUE

    """ Oracle for numerology """
    STOPWORDS = set(stopwords.words('english'))

    NUMEROLOGICAL_NAME_VALUE = 0

    NUMVALUES = {"a": 1, "j": 1, "s": 1, "b": 2, "k": 2, "t": 2, "c": 3, "l": 3, "u": 3, "d": 4, "m": 4, "v": 4,
                 "e": 5, "n": 5, "w": 5, "f": 6, "o": 6, "x": 6, "g": 7, "p": 7, "y": 7, "h": 8, "q": 8, "z": 8,
                 "i": 9, "r": 9}

    # EIGHTBALL = ("It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
    #             "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
    #             "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
    #             "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
    #             "Don't count on it.", "My reply is no.", "My sources say no.",
    #             "Outlook not so good.", "Very doubtful.")

    # The timeframe representing universal stability (seconds)
    STABLE_UNIVERSE_TIMEFRAME = 300

    # Number of seconds of stability the prediction will have.
    TIMEFRAME = STABLE_UNIVERSE_TIMEFRAME

    def get_numerological_value(self, word):
        # https://en.wikipedia.org/wiki/Numerology#Latin_alphabet_systems
        digits = str(sum([self.NUMVALUES[l]
                          for l in word.lower() if l in self.NUMVALUES.keys()]))

        value = int(digits) % 9

        if value == 0:
            value = 9

        return value

    def get_prophecy(self, question):

        # Strip junk and junk words, get rng seed from numerological sum, then weight against current time.
        words = list(filter(lambda word: word not in self.STOPWORDS,
                            re.sub("[^a-z0-9 ]+", "", question.lower()).split()))

        total = sum(self.get_numerological_value(word) for word in words)
        random.seed(total + int(time.time()/self.TIMEFRAME))
        answer = random.choice(self.EIGHTBALL)

        # How far away we are from the self.STABLE_UNIVERSE_TIMEFRAME determines
        # the proportion of significance (in absolute) terms that this
        # prophecy describes.
        #
        # The significance must be between -1.0 <= significance <= 1.0
        significance = max(-1.0, min(1.0, self.NUMEROLOGICAL_NAME_VALUE /
                                     self.STABLE_UNIVERSE_TIMEFRAME))

        return NumerologyProphecy(self, significance, answer)

#
#   ASTROLOGY
#


class AstrologyProphecy(ProphecyBase):
    """ A prophecy by the oracles of the Astrology school """
    pass


class AstrologyOracle(OracleBase):

    def __init__(self, school, oracle_name):
        super().__init__(school, oracle_name)

        # TODO - Add zodiac houses

    def get_prophecy(self, question):
        """ Gets the prophecy from this astrology oracle """
        return super().get_prophecy(question)


class YiJingOracle(OracleBase):

    ten_wings_commentary = []

    def __init__(self, school, oracle_name):
        super().__init__(school, oracle_name)
        self.ten_wings_commentary = read_json(
            "better-magic8ball.prophecies.json")["yijing"]

    def throw_coins(self, num_coins=3):
        """ Throws num_coins to work out how the yao stacked line looks """

        coins = []
        for i in range(0, num_coins):
            if get_time_millis() % 2 == 0:
                # Heads
                coins.append(2)
            else:
                # Tails
                coins.append(3)

        return coins

    def get_yao_stacked_line(self):
        """
        Gets a yao stacked line and whether it's broken or not based on the time
        """

        coins_total = sum(self.throw_coins())
        return coins_total

    def get_zhou_yi(self):
        return [
            self.get_yao_stacked_line(),    # Line 6 - Top
            self.get_yao_stacked_line(),    # Line 5
            self.get_yao_stacked_line(),    # Line 4
            self.get_yao_stacked_line(),    # Line 3
            self.get_yao_stacked_line(),    # Line 2
            self.get_yao_stacked_line()     # Line 1 - Base
        ]

    def choose_prophecy_text(self, yao):

        num_choices = len(self.ten_wings_commentary)
        zhou_yi_primary = yao['primary']
        zhou_yi_secondary = yao['secondary']

        cosmic_random = random.SystemRandom()
        has_entropy = False
        prophecy_text = cosmic_random.choice(self.ten_wings_commentary)
        min_sentence_length = 50   # characters
        max_sentence_length = 180  # characters
        num_iterations = 0

        while not has_entropy:
            prophecy_candidate = cosmic_random.choice(
                self.ten_wings_commentary)

            if 2 + len(prophecy_text) + len(prophecy_candidate) <= max_sentence_length:
                prophecy_text = "{}. {}".format(
                    prophecy_text, prophecy_candidate)

            enough_said = (cosmic_random.randint(num_iterations, 5) % 2 == 0)
            if len(prophecy_text) >= (max_sentence_length - min_sentence_length) or enough_said:
                has_entropy = True

        return "{}.".format(prophecy_text)

    def get_prophecy(self, question):
        """
        Gets the prophecy according to Yi Jing or I Ching casting of lots
        https://en.wikipedia.org/wiki/I_Ching displayed on a Zhou yi board

        ...The basic unit of the Zhou yi is the hexagram (卦 guà), a figure
        composed of six stacked horizontal lines (爻 yáo). Each line is either
        broken or unbroken...

        https://www.eclecticenergies.com/iching/introduction
        ...Hexagrams are sets of six lines, that can be broken _ _ or unbroken
        ___. The broken lines are "yin," the unbroken lines "yang." Something
        it is yin when it is female or dark, earthly, passive etc. and yang when
        it is male or light, heavenly, active etc.

        | coins	            | total | line	|     | changing   |
        |-------------------|-------|-------|-----|------------|
        | 0 heads + 3 tails |   6   | yin   | _ _ | changing   |
        | 1 heads + 2 tails |   7   | yang  | ___ | static     |
        | 2 heads + 1 tails |   8   | yin   | _ _ | static     |
        | 3 heads + 0 tails |   9   | yang  | ___ | changing   |

        """

        # Set up the divination boards
        zhou_yi_primary = self.get_zhou_yi()
        zhou_yi_secondary = self.get_zhou_yi()

        # Get the zhou_yi of change
        zhou_yi = []
        for i in range(0, 6):
            if zhou_yi_primary[i] in [6, 9] and zhou_yi_secondary[i] in [6, 9]:
                zhou_yi.append(12)  # Changing
            else:
                zhou_yi.append(0)  # Static

        significance = (float(sum(zhou_yi)) / float(100))

        return ProphecyBase(self, significance,
                            self.choose_prophecy_text({
                                "primary": zhou_yi_primary,
                                "secondary": zhou_yi_secondary
                            }))


class Pantheon:
    """ The Pantheon is the set of Oracles from all the Schools of Mythology """
    oracles = []

    response_types = []

    def __init__(self, oracles):
        """ Initialises the pantheon of Oracles to be able to perform prophecies """
        self.oracles = oracles

    def pose_question(self, question):
        """
        Poses a question to all oracles and returns the prophecies as foretold
        by the oracles
        """
        prophecies = []
        for oracle in self.oracles:
            prophecy = oracle.get_prophecy(question)
            prophecies.append(prophecy)

        # Sort by significance (descending) and return the top result
        prophecies.sort(key=lambda x: x.get_significance(), reverse=True)

        return prophecies


def get_answer_to_question(question):
    """ Gets all the answers, chooses a prophecy and returns its text """
    answers = get_all_answers_to_question(question)

    cosmic_random = random.SystemRandom()
    response_type = cosmic_random.randint(0, 2)

    if response_type == 0:
        return answers[0].get_prophecy_text()

    elif response_type == 1:
        return "According to {} the answer is \"{}\"".format(
            answers[0].get_oracle().oracle_name,
            answers[0].get_prophecy_text()
        )

    elif response_type == 2:
        return "According to {} the answer is \"{}\" and according to {} it is \"{}\"".format(
            answers[0].get_oracle().oracle_name,
            answers[0].get_prophecy_text(),
            answers[1].get_oracle().oracle_name,
            answers[1].get_prophecy_text()
        )

    return answers[0].get_prophecy_text()


def get_all_answers_to_question(question):
    """ Gets all the answers to a question """
    oracles = [
        #AstrologyOracle("Astrology", "Zodiac Houses"),
        NumerologyOracle("Numerology", "Latin Numerology"),
        NumerologyOracle("Numerology", "Modern Numerology"),
        YiJingOracle("Cleromancy", "Ten Wings of Yi Jing")
        #  Add more Oracles here
    ]
    pantheon = Pantheon(oracles)
    answers = pantheon.pose_question(question)

    return answers


def get_time_millis():
    """ Gets the time in milliseconds """
    try:
        return time.time_ns()
    except NameError:
        return (time.time() * 1000)


def read_contents(filename):
    module_path = Path(__file__).parent
    abs_filename = Path(module_path, filename)  # module_path/filename
    with open(abs_filename.absolute(), 'r') as fin:
        return fin.read()


def write_contents(filename, contents, overwrite=True):
    module_path = Path(__file__).parent
    abs_filename = Path(module_path, filename)
    with open(abs_filename.absolute(), "w") as fout:
        fout.write(contents)


def read_json(filename):
    return json.loads(read_contents(filename))


def write_json(filename, content, overwrite=True):
    write_contents(filename, json.dumps(content, indent=4), overwrite)


try:
    import sopel.module
except ImportError:
    pass
else:
    @sopel.module.commands('q')
    @sopel.module.example('.q some question')
    def f_ask_question(bot, trigger):
        """ Ask the Magic 8 ball a question """
        if trigger.group(2):
            answer = get_answer_to_question(trigger.group(2))
            bot.say('The 8-ball responds: {}'.format(answer), trigger.sender)
        else:
            bot.say('Try asking a question.', trigger.sender)
        return sopel.module.NOLIMIT

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print("The query is '{}'".format(query))
        answer = get_answer_to_question(query)
        print("The answer is '{}'".format(answer))

        print('Asking again for all prophecies:')
        answers = get_all_answers_to_question(query)
        for p in answers:
            print("    Significance: {:+.2%} '{}'".format(
                p.get_significance(), p.get_prophecy_text()))

    else:
        print("{}: No question given.".format(sys.argv[0]))
