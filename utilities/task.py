import datetime
from enum import Enum
from abc import ABC, abstractmethod
from termcolor import colored
import random


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

    def __init__(self, task_id, name, length, subjects, difficulty, color):
        super(Task, self).__init__()
        self.color = color
        self.subjects = subjects
        self.task_id = task_id
        self.is_terminated = False
        self.name = name
        self.progress = 0
        self.previous_progress = -100000    # initialized to a very negative number
        self.length = length
        self.difficulty = difficulty        # value from 0 to 5

    @abstractmethod
    def execute(self, value):
        pass

    @abstractmethod
    def metric(self, state):

        """ metric function used by agent to compute its fitness
            based on the current state of the agent itself """
        pass

    def print_progress(self):

        """ print the progress of the current task execution """

        percentage = (self.progress * 100) / self.length
        print(colored('{' + str(datetime.datetime.now().time()) + '}', "grey"),
              colored('             [' + self.name + ']' + ' execution ' + str(percentage) + '% complete..', color=self.color))


class CookTask(Task):

    def __init__(self, task_id, name, length,difficulty, color):
        super(CookTask, self).__init__(task_id=task_id,
                                       name=name,
                                       length=length,
                                       subjects=[Subject.COOKERS, Subject.KITCHEN, Subject.INGREDIENTS],
                                       difficulty=difficulty,
                                       color=color)

    def execute(self, value):
        self.previous_progress = self.progress
        self.progress += value
        if self.progress >= self.length:
            self.is_terminated = True
        self.print_progress()

    # TODO: change the metric
    def metric(self, state):
        return random.randint(0, 100)


class DishOutTask(Task):

    def __init__(self, task_id, name, length, difficulty, color):
        super(DishOutTask, self).__init__(task_id=task_id,
                                          name=name,
                                          length=length,
                                          subjects=[Subject.DISH, Subject.TRAYS],
                                          difficulty=difficulty,
                                          color=color)

    def execute(self, value):
        self.progress += value
        if self.progress >= self.length:
            self.is_terminated = True
        self.print_progress()

    # TODO: change the metric
    def metric(self, state):
        return random.randint(0, 100)
