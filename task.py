import random

from utility import Topic, Subject, Logger, MAX_ID
from abc import ABC, abstractmethod
from termcolor import cprint


class Task(ABC):

    """ Abstract representation of a single Task """

    BASE_NAME = "task"

    def __init__(self,
                 name,
                 length,
                 subjects,
                 min_progress,
                 difficulty,
                 color="grey",
                 write_on_terminal=True,
                 verbose=True,
                 attrs=None,
                 level=3):

        super(Task, self).__init__()

        # task information
        self.logger = Logger(name, color, attrs, write_on_terminal, verbose, level)
        self.task_id = Task.BASE_NAME + str(random.randint(0, MAX_ID))
        self.length = length
        if subjects is None:
            subjects = []
        self.subjects = subjects
        self.difficulty = difficulty

        # task progress
        self.min_progress = min_progress
        self.progress = 0
        self.previous_progress = -1000000
        self.terminated = False

    @abstractmethod
    def metric(self, skill):
        """ metric function that given the skills of the agent
            returns a fitness score representing how much the
            agent is good for doing this task """
        pass

    def execute(self, value):

        """ execute the task, increasing the progress """

        self.previous_progress = self.progress
        self.progress += value
        self.__print_progress()
        self.__check_termination()

    def __check_termination(self):

        """ checks whether the task is terminated or not """

        if self.progress >= self.length:
            self.terminated = True

    def __print_progress(self):
        percentage = (self.progress * 100) / self.length

        if percentage <= 100:
            self.logger.log(message="execution {perc}% complete".format(perc=percentage))
        else:
            self.logger.log(message="task completed!!!!  <---------", kind='e')


class CookTask(Task):

    def __init__(self, name, length, min_progress, difficulty,
                 color="grey", write_on_terminal=True, verbose=True, attrs=None):
        super(CookTask, self).__init__(name=name,
                                       length=length,
                                       subjects=[Subject.COOKERS, Subject.KITCHEN, Subject.INGREDIENTS],
                                       min_progress=min_progress,
                                       difficulty=difficulty,
                                       color=color,
                                       write_on_terminal=write_on_terminal,
                                       verbose=verbose,
                                       attrs=attrs)

    def metric(self, skill):

        # linear combination among all abilities but cleverness
        deterministic_fitness = 0.5 * 20 * skill.stars + 0.4 * skill.energy + 0.1 * skill.speed
        random_fitness = random.randint(0, 30)

        return deterministic_fitness + random_fitness


class DishOutTask(Task):

    def __init__(self, name, length, min_progress, difficulty,
                 color="grey", write_on_terminal=True, verbose=True, attrs=None):
        super(DishOutTask, self).__init__(name=name,
                                          length=length,
                                          subjects=[Subject.DISH, Subject.TRAYS],
                                          min_progress=min_progress,
                                          difficulty=difficulty,
                                          color=color,
                                          write_on_terminal=write_on_terminal,
                                          verbose=verbose,
                                          attrs=attrs)

    def metric(self, skill):

        # linear combination among all abilities but stars
        deterministic_fitness = 0.1 * skill.cleverness + 0.4 * skill.energy + 0.5 * skill.speed
        random_fitness = random.randint(0, 20)

        return deterministic_fitness + random_fitness


class HandlePaymentTask(Task):

    def __init__(self, name, length, min_progress, difficulty,
                 color="grey", write_on_terminal=True, verbose=True, attrs=None):
        super(HandlePaymentTask, self).__init__(name=name,
                                                length=length,
                                                subjects=[Subject.DISH, Subject.TRAYS],
                                                min_progress=min_progress,
                                                difficulty=difficulty,
                                                color=color,
                                                write_on_terminal=write_on_terminal,
                                                verbose=verbose,
                                                attrs=attrs)

    def metric(self, skill):

        # linear combination among all abilities but stars
        deterministic_fitness = 0.7 * skill.cleverness + 0.2 * skill.energy + 0.1 * skill.speed
        random_fitness = random.randint(0, 30)

        return deterministic_fitness + random_fitness
