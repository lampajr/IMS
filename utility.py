import random
import time
from enum import Enum
from abc import ABC, abstractmethod
from termcolor import cprint


MAX_ID = 500


class Logger:
    """ Abstract logger class """

    ERROR = "red"

    def __init__(self, name, color, attrs, write_on_terminal, verbose, level):
        super(Logger, self).__init__()
        self.name = name.upper()
        self.color = color
        if attrs is None:
            attrs = []
        self.attrs = attrs
        self.write_on_terminal = write_on_terminal
        self.verbose = verbose
        self.level = level

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


class Topic(Enum):
    """ Topics enumeration """

    COOK = 'cook'
    HANDLE_PAYMENTS = 'handle_payments'
    DISH_OUT = 'dish_out'


class Subject(Enum):
    """ Subjects enumeration: resources available """

    CASH_DESK = 0
    COOKERS = 1
    INGREDIENTS = 2
    KITCHEN = 3
    TRAYS = 4
    DISH = 5


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
    elif topic == Topic.DISH_OUT:
        return [Subject.CASH_DESK]


def get_topic(subjects):

    """ function that given the list of subjects returns
        the corresponding topic over which negotiate """

    if Subject.COOKERS in subjects and Subject.KITCHEN in subjects and Subject.INGREDIENTS in subjects:
        return Topic.COOK
    elif Subject.DISH in subjects and Subject.TRAYS in subjects:
        return Topic.DISH_OUT
    elif Subject.CASH_DESK in subjects:
        return Topic.HANDLE_PAYMENTS
    else:
        print('There are no valid resources!!')
