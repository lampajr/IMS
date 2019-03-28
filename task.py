import datetime
from enum import Enum
from abc import ABC, abstractmethod
from termcolor import colored
import random

from auctioneer import generate_auctioneer


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


class Task(ABC):

    """ Abstract Task class """

    def __init__(self, task_id, name, length, subjects, difficulty,
                 color, attrs=None, write_on_terminal=False):
        super(Task, self).__init__()
        if attrs is None:
            attrs = []
        self.attrs = attrs
        self.write_on_terminal = write_on_terminal
        self.color = color
        self.subjects = subjects
        self.task_id = task_id
        self.is_terminated = False
        self.name = name
        self.progress = 0
        self.previous_progress = -100000    # initialized to a very negative number
        self.length = length
        self.difficulty = difficulty        # value from 0 to 5

    def execute(self, value):
        self.previous_progress = self.progress
        self.progress += value
        if self.progress >= self.length:
            self.trigger_subtask()
            self.is_terminated = True
        self.print_progress()

    @abstractmethod
    def metric(self, state):

        """ metric function used by agent to compute its fitness
            based on the current state of the agent itself """
        pass

    @abstractmethod
    def create_subtask(self):
        pass

    def print_progress(self):

        """ print the progress of the current task execution """

        percentage = (self.progress * 100) / self.length
        if percentage > 100:
            percentage = 100

        if self.write_on_terminal:
            print(colored('{' + str(datetime.datetime.now().time()) + '}', color="grey", attrs=self.attrs),
                  colored('             [' + self.name + ']' + ' execution ' + str(percentage) + '% complete..',
                          color=self.color, attrs=self.attrs))
        else:
            with open("output.txt", "a+") as f:
                message = '{' + str(datetime.datetime.now().time()) + '}' + "                   [" + self.name +\
                          "] execution " + str(percentage) + "% complete..\n"
                f.write(message)

    def trigger_subtask(self):
        task = self.create_subtask()
        if task is None:
            return
        auctioneer = generate_auctioneer()
        auctioneer.trigger_task(task=task)


class CookTask(Task):

    PREFIX = "cook"

    def __init__(self, task_id, name, length,difficulty, color):
        super(CookTask, self).__init__(task_id=task_id,
                                       name=CookTask.PREFIX + " " + name,
                                       length=length,
                                       subjects=[Subject.COOKERS, Subject.KITCHEN, Subject.INGREDIENTS],
                                       difficulty=difficulty,
                                       color=color)


    def metric(self, state):

        """ for this application I've thought to consider random fitness metric
            in order to have an unpredictable behavior """

        return random.randint(0, 100)

    def create_subtask(self):
        return DishOutTask(task_id="d" + random.randint(0, 500),
                           name=self.name,
                           length=DishOutTask.LENGTH,
                           difficulty=DishOutTask.DIFFICULTY,
                           color=self.color,
                           attrs=['underline'],
                           write_on_terminal=self.write_on_terminal)


class DishOutTask(Task):

    PREFIX = "dish out"
    LENGTH = 150
    DIFFICULTY = 3

    def __init__(self, task_id, name, length, difficulty, color, attrs, write_on_terminal):
        super(DishOutTask, self).__init__(task_id=task_id,
                                          name=DishOutTask.PREFIX + " " + name,
                                          length=length,
                                          subjects=[Subject.DISH, Subject.TRAYS],
                                          difficulty=difficulty,
                                          color=color,
                                          attrs=attrs,
                                          write_on_terminal=write_on_terminal)

    def metric(self, state):
        return random.randint(0, 100)

    def create_subtask(self):
        return HandlePaymentTask(task_id="h" + random.randint(0, 500),
                                 name=HandlePaymentTask.PREFIX + " " + self.name,
                                 length=HandlePaymentTask.LENGTH,
                                 subjects=[Subject.CASH_DESK],
                                 difficulty=HandlePaymentTask.DIFFICULTY,
                                 color=self.color,
                                 attrs=['bold'],
                                 write_on_terminal=self.write_on_terminal)


class HandlePaymentTask(Task):

    PREFIX = "pay"
    LENGTH = 100
    DIFFICULTY = 1

    def __init__(self, task_id, name, length, subjects, difficulty, color, attrs, write_on_terminal):
        super(HandlePaymentTask, self).__init__(task_id=task_id,
                                                name=HandlePaymentTask.PREFIX + " " + name,
                                                length=length,
                                                subjects=[Subject.CASH_DESK],
                                                difficulty=difficulty,
                                                color=color,
                                                attrs=attrs,
                                                write_on_terminal=write_on_terminal)

    def metric(self, state):
        return random.randint(0, 100)

    def create_subtask(self):
        return None
