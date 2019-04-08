import random
import time
from enum import Enum
from termcolor import cprint

MAX_ID = 500


class Logger:
    """ Abstract logger class """

    ERROR = "red"

    def __init__(self,
                 name,
                 color,
                 attrs,
                 write_on_terminal,
                 verbose,
                 level,
                 use_time=True,
                 description=None):
        super(Logger, self).__init__()
        self.name = name.upper()
        self.color = color
        if attrs is None:
            attrs = []
        self.attrs = attrs
        self.write_on_terminal = write_on_terminal
        self.verbose = verbose
        self.level = level
        self.use_time = use_time
        self.description = description

    def log(self, message, kind="d", level=0):

        """ logger function
            kind: 'd' -> debug, 'e' -> error
            level: int -> how many tabs to indent """

        if self.verbose:
            if self.write_on_terminal:
                self.tlog(kind=kind, message=message)
            else:
                self.flog(kind=kind, message=message)

    def get_log_color(self, kind):
        return Logger.ERROR if kind == 'e' \
            else "grey" if self.color is None else self.color

    def tlog(self, message, kind):

        """ log the information on the terminal """

        color = self.get_log_color(kind=kind)
        text = 2 * self.level * "    " + "[" + self.name + "]    " + message
        cprint(text=text, color=color, attrs=self.attrs)

    def flog(self, message, kind):

        """ log information on the file """

        pass


class Skill:

    """ represents the skills of an agent """

    def __init__(self, energy=100, cleverness=0, speed=0, stars=0):
        self.energy = energy            # value from 0 to 100
        self.cleverness = cleverness    # value from 0 to 100
        self.speed = speed              # value from 0 to 100
        self.stars = stars              # michelin's star 0 to 3


class Topic(Enum):
    """ Topics enumeration """

    COOK = 'cook'
    HANDLE_PAYMENTS = 'handle_payments'
    SERVE = 'serve'


class Subject(Enum):
    """ Subjects enumeration: resources available """

    CASH_DESK = 0
    COOKERS = 1
    INGREDIENTS = 2
    KITCHEN = 3
    TRAYS = 4
    DISH = 5


class MessageType(Enum):
    ANNOUNCEMENT = 0
    BID = 1
    CLOSE = 2
    RENEWAL = 3
    ACKNOWLEDGEMENT = 4


def get_time():
    return int(round(time.time() * 1000))


def get_color(color):

    """ return a random color string different from the argument """

    lst = ['green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    dim = len(lst) - 1
    new_color = color
    while new_color == color:
        idx = random.randint(0, dim)
        new_color = lst[idx]
    return new_color


def get_subjects(topic):

    """ provide list of subject required given a topic """

    if topic == Topic.COOK:
        return [Subject.COOKERS, Subject.KITCHEN, Subject.INGREDIENTS]
    elif topic == Topic.HANDLE_PAYMENTS:
        return [Subject.TRAYS, Subject.DISH]
    elif topic == Topic.SERVE:
        return [Subject.CASH_DESK]


def get_topic_from_subjects(subjects):

    """ function that given the list of subjects returns
        the corresponding topic over which negotiate """

    if Subject.COOKERS in subjects and Subject.KITCHEN in subjects and Subject.INGREDIENTS in subjects:
        return Topic.COOK
    elif Subject.DISH in subjects and Subject.TRAYS in subjects:
        return Topic.SERVE
    elif Subject.CASH_DESK in subjects:
        return Topic.HANDLE_PAYMENTS
    else:
        print('There are no valid resources!!')


def get_topic_from_string(name):

    """ given a string returns its topic """

    if name == "cook":
        return Topic.COOK
    elif name == "serve":
        return Topic.SERVE
    elif name == "handle_payments":
        return Topic.HANDLE_PAYMENTS


def get_boolean(value):

    """ convert a string into boolean obj """

    return value == "True" or value == "true"


def create_skill(skill_elements):

    """ given a '-' separated list of values returns a new skill obj """

    elements = skill_elements.split('-')
    return Skill(energy=int(elements[0]),
                 cleverness=int(elements[1]),
                 speed=int(elements[2]),
                 stars=int(elements[3]))
